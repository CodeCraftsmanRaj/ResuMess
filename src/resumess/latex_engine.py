from __future__ import annotations

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


def render_resume_pdf(body_latex: str, output_dir: str | Path, file_name: str = "resume") -> Path:
    """Generate `.tex` and compile PDF using local LaTeX tools through `pylatex`."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    doc = build_document(body_latex, title="Resume")
    doc.generate_pdf(filepath=str(output_path / file_name), clean_tex=False)
    return output_path / f"{file_name}.pdf"


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
