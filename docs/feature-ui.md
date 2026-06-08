# Feature: UI

## Goal
Build the frontend experience for ResuMess.

## Scope
- Resume editor shell
- JD input panel
- Live preview area
- Download actions
- Navigation for future modules

## LaTeX Integration Requirements
- Call `POST /latex/render` when user clicks Generate/Update
- Show compile status states: `queued`, `compiling`, `compiled`, `failed`
- Embed preview from `GET /latex/preview/{docId}`
- Provide download actions for `pdf` and `tex`
- Render compile diagnostics with line-level hints when available

## Acceptance Criteria
- User can generate and preview a PDF in one flow
- Compile errors are readable and actionable in UI
- Download buttons are visible only for successful artifacts
- Previous successful preview remains visible on failed recompilation

## Notes
This branch stays focused on presentation and workflow entry points only.
