# LaTeX Integration Stack: `pylatex` + Overleaf

## Decision
ResuMess LaTeX integration is standardized on Python's `pylatex` for generation and compile orchestration, with Overleaf-compatible export bundles for cloud editing and collaboration.

## Why `pylatex`
- Python-native document construction
- Programmatic template assembly
- Controlled compile flow and artifact handling
- Easy integration with backend services

## Overleaf Usage
- Export generated `.tex` (and assets) as a ZIP bundle
- Import ZIP into Overleaf for collaborative edits
- Keep the same template structure between local compile and Overleaf

## Initial API Surface
- `build_document()` -> constructs `pylatex.Document`
- `render_resume_pdf()` -> compiles PDF and retains `.tex`
- `export_overleaf_bundle()` -> ZIP for Overleaf import

## Security and Stability Notes
- Sanitize dynamic title fields before injection
- Keep compile in restricted worker/runtime
- Track `.log` output for safe diagnostics
- Do not expose raw filesystem paths in API responses
