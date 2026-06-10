from __future__ import annotations

import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from pylatex import Document, NoEscape


def build_document(body_latex: str, title: str = "ResuMess Document") -> Document:
    """Create a minimal LaTeX document using `pylatex`."""
    doc = Document(documentclass="article")
    doc.preamble.append(NoEscape(r"\title{" + title.replace("{", "").replace("}", "") + "}"))
    doc.preamble.append(NoEscape(r"\date{}"))
    doc.append(NoEscape(r"\maketitle"))
    doc.append(NoEscape(body_latex))
    return doc


def is_latex_installed() -> bool:
    """Check if LaTeX compiler (pdflatex/latexmk) is installed locally."""
    return shutil.which("pdflatex") is not None or shutil.which("latexmk") is not None


def render_resume_pdf_local(body_latex: str, output_dir: str | Path, file_name: str = "resume") -> Path:
    """Generate `.tex` and compile PDF using local LaTeX tools through `pylatex`."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    doc = build_document(body_latex, title="Resume")
    doc.generate_pdf(filepath=str(output_path / file_name), clean_tex=False)
    return output_path / f"{file_name}.pdf"


def render_resume_pdf_mock(body_latex: str, output_dir: str | Path, file_name: str = "resume") -> Path:
    """Generate a mock PDF for testing (when LaTeX compiler is unavailable).
    
    This creates a simple PDF with the LaTeX source embedded as text.
    Useful for development without installing LaTeX.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    doc = build_document(body_latex, title="Resume")
    
    # Write .tex file
    tex_path = output_path / f"{file_name}.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(doc.dumps())
    
    # Create a mock PDF using reportlab
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        pdf_path = output_path / f"{file_name}.pdf"
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "ResuMess Generated Resume (Mock PDF)")
        
        # Separator
        c.setFont("Helvetica", 10)
        c.drawString(50, 730, "-" * 80)
        
        # LaTeX Source Preview
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 700, "LaTeX Source:")
        
        c.setFont("Courier", 9)
        y = 680
        for i, line in enumerate(body_latex.split("\n")[:30]):  # Show first 30 lines
            if y < 50:
                break
            c.drawString(50, y, line[:100])  # Truncate long lines
            y -= 15
        
        c.save()
        return pdf_path
    
    except ImportError:
        # If reportlab not available, create minimal PDF manually
        pdf_path = output_path / f"{file_name}.pdf"
        
        # Minimal PDF structure
        pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
5 0 obj
<< /Length 100 >>
stream
BT
/F1 12 Tf
50 750 Td
(ResuMess Resume - Mock PDF) Tj
ET
endstream
endobj
xref
0 6
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000214 00000 n
0000000301 00000 n
trailer
<< /Size 6 /Root 1 0 R >>
startxref
451
%%EOF
"""
        with open(pdf_path, "wb") as f:
            f.write(pdf_content)
        
        return pdf_path


def render_resume_pdf(body_latex: str, output_dir: str | Path, file_name: str = "resume") -> Path:
    """Generate `.tex` and compile PDF using available method.
    
    Priority:
    1. Local LaTeX compiler (pdflatex/latexmk) if installed
    2. Mock PDF generator (for testing without LaTeX)
    """
    if is_latex_installed():
        return render_resume_pdf_local(body_latex, output_dir, file_name)
    else:
        return render_resume_pdf_mock(body_latex, output_dir, file_name)


def export_overleaf_bundle(tex_file: str | Path, output_zip: str | Path) -> Path:
    """Bundle LaTeX sources for Overleaf import.

    Overleaf accepts ZIP uploads containing `.tex` and related assets.
    """
    tex_path = Path(tex_file)
    if not tex_path.exists():
        raise FileNotFoundError(f"Missing source file: {tex_path}")

    output_zip_path = Path(output_zip)
    output_zip_path.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output_zip_path, "w", ZIP_DEFLATED) as zf:
        zf.write(tex_path, arcname=tex_path.name)

    return output_zip_path
