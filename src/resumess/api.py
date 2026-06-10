"""FastAPI HTTP layer for LaTeX rendering and compilation."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .latex_engine import render_resume_pdf, export_overleaf_bundle


# ============================================================================
# Enums
# ============================================================================

class DocumentType(str, Enum):
    """Supported document types."""
    resume = "resume"
    cv = "cv"
    sop = "sop"


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    error = "error"
    warning = "warning"


# ============================================================================
# Pydantic Request/Response Models
# ============================================================================

class RenderMetadata(BaseModel):
    """Optional metadata about the document context."""
    company: str | None = None
    role: str | None = None
    jdHash: str | None = None


class RenderRequest(BaseModel):
    """Request payload for rendering LaTeX to PDF."""
    userId: str = Field(..., description="User ID")
    documentType: DocumentType = Field(..., description="Type of document")
    templateId: str = Field(default="jakes", description="Template identifier")
    latexSource: str = Field(..., description="Raw LaTeX source code")
    meta: RenderMetadata | None = Field(default=None, description="Optional metadata")


class CompileError(BaseModel):
    """A single compilation error or warning."""
    line: int | None = Field(None, description="Line number of error (if available)")
    message: str = Field(..., description="Error message")
    severity: ErrorSeverity = Field(..., description="Error severity level")


class DownloadLinks(BaseModel):
    """Links to downloadable artifacts."""
    pdf: str = Field(..., description="URL to download PDF")
    tex: str = Field(..., description="URL to download LaTeX source")
    log: str = Field(..., description="URL to download compilation log")


class RenderSuccessResponse(BaseModel):
    """Successful render response."""
    docId: str = Field(..., description="Unique document ID")
    status: Literal["compiled"] = "compiled"
    previewUrl: str = Field(..., description="URL to preview PDF")
    downloads: DownloadLinks = Field(..., description="Download links for artifacts")


class RenderFailureResponse(BaseModel):
    """Failed render response."""
    status: Literal["failed"] = "failed"
    errorSummary: str = Field(..., description="Summary of compilation failure")
    errors: list[CompileError] = Field(default_factory=list, description="List of errors")


# ============================================================================
# In-Memory Storage (upgrade to database later)
# ============================================================================

class DocumentMetadata(BaseModel):
    """Stored metadata for a document."""
    docId: str
    userId: str
    documentType: DocumentType
    templateId: str
    createdAt: datetime
    texFilePath: Path
    pdfFilePath: Path
    logFilePath: Path | None = None
    meta: RenderMetadata | None = None


# Global document store (use DB in production)
document_store: dict[str, DocumentMetadata] = {}
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="ResuMess LaTeX Engine",
    description="HTTP API for rendering, compiling, and previewing LaTeX resumes",
    version="0.1.0",
)


# ============================================================================
# Utility Functions
# ============================================================================

def generate_doc_id() -> str:
    """Generate a unique document ID."""
    return f"doc_{uuid.uuid4().hex[:12]}"


def parse_latex_errors(log_content: str) -> list[CompileError]:
    """Extract compilation errors from LaTeX log file.
    
    This is a simplified parser. A production version would parse:
    - Line numbers
    - Error types (Undefined control sequence, Missing $, etc.)
    - Severity levels
    """
    errors = []
    
    # Simple heuristic: look for "!" which indicates errors in LaTeX
    for i, line in enumerate(log_content.split("\n"), 1):
        if line.strip().startswith("!"):
            errors.append(
                CompileError(
                    line=i,
                    message=line.strip(),
                    severity=ErrorSeverity.error,
                )
            )
    
    return errors


# ============================================================================
# Endpoints
# ============================================================================

@app.post(
    "/latex/render",
    response_model=RenderSuccessResponse | RenderFailureResponse,
    status_code=200,
)
async def render_latex(request: RenderRequest) -> RenderSuccessResponse | RenderFailureResponse:
    """
    Render and compile LaTeX to PDF.
    
    **Request Body:**
    - `userId`: Your user ID
    - `documentType`: Type of document (resume, cv, sop)
    - `templateId`: Which template to use (default: "jakes")
    - `latexSource`: Raw LaTeX code to compile
    - `meta`: Optional metadata (company, role, jdHash)
    
    **Returns (Success 200):**
    - `docId`: Unique ID to reference this document
    - `previewUrl`: Where to view the PDF
    - `downloads`: Links to PDF, TEX, and LOG files
    
    **Returns (Failure):**
    - `status`: "failed"
    - `errorSummary`: What went wrong
    - `errors`: List of compilation errors with line numbers
    """
    try:
        # Generate unique document ID
        doc_id = generate_doc_id()
        
        # Create artifacts directory
        doc_dir = ARTIFACTS_DIR / doc_id
        doc_dir.mkdir(parents=True, exist_ok=True)
        
        # Compile LaTeX to PDF
        pdf_path = render_resume_pdf(
            body_latex=request.latexSource,
            output_dir=doc_dir,
            file_name="resume",
        )
        
        # Get tex file path
        tex_path = doc_dir / "resume.tex"
        
        # Store metadata
        metadata = DocumentMetadata(
            docId=doc_id,
            userId=request.userId,
            documentType=request.documentType,
            templateId=request.templateId,
            createdAt=datetime.now(),
            texFilePath=tex_path,
            pdfFilePath=pdf_path,
            meta=request.meta,
        )
        document_store[doc_id] = metadata
        
        # Return success response
        return RenderSuccessResponse(
            docId=doc_id,
            previewUrl=f"/latex/preview/{doc_id}",
            downloads=DownloadLinks(
                pdf=f"/latex/download/{doc_id}?type=pdf",
                tex=f"/latex/download/{doc_id}?type=tex",
                log=f"/latex/download/{doc_id}?type=log",
            ),
        )
    
    except Exception as e:
        # Try to extract errors from log file if it exists
        log_file = doc_dir / "resume.log"
        errors = []
        if log_file.exists():
            log_content = log_file.read_text()
            errors = parse_latex_errors(log_content)
        
        return RenderFailureResponse(
            errorSummary=f"LaTeX compilation failed: {str(e)}",
            errors=errors,
        )


@app.get("/latex/preview/{docId}")
async def preview_latex(docId: str) -> FileResponse:
    """
    Preview a compiled PDF.
    
    **Parameters:**
    - `docId`: Document ID from render response
    
    **Returns:**
    - PDF file as a stream (viewable in browser)
    """
    # Validate document exists
    if docId not in document_store:
        raise HTTPException(
            status_code=404,
            detail=f"Document {docId} not found",
        )
    
    metadata = document_store[docId]
    
    # Check if PDF exists
    if not metadata.pdfFilePath.exists():
        raise HTTPException(
            status_code=404,
            detail=f"PDF not found for document {docId}",
        )
    
    # Return PDF as inline preview
    return FileResponse(
        path=metadata.pdfFilePath,
        media_type="application/pdf",
        filename=f"resume.pdf",
    )


@app.get("/latex/download/{docId}")
async def download_artifact(
    docId: str,
    type: Literal["pdf", "tex", "log"] = Query(..., description="Artifact type to download"),
) -> FileResponse:
    """
    Download a document artifact (PDF, TEX source, or LOG file).
    
    **Parameters:**
    - `docId`: Document ID from render response
    - `type`: Which file to download (pdf, tex, log)
    
    **Returns:**
    - Requested file as an attachment (prompts browser to download)
    """
    # Validate document exists
    if docId not in document_store:
        raise HTTPException(
            status_code=404,
            detail=f"Document {docId} not found",
        )
    
    metadata = document_store[docId]
    
    # Map type to file path
    file_map = {
        "pdf": metadata.pdfFilePath,
        "tex": metadata.texFilePath,
        "log": metadata.texFilePath.parent / "resume.log",
    }
    
    file_path = file_map[type]
    
    # Validate file exists
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{type.upper()} file not found for document {docId}",
        )
    
    # Return file as attachment
    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=f"resume.{type}",
    )


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "latex-engine"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
