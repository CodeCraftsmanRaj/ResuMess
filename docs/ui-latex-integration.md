# UI Integration: LaTeX Render Flow

## Flow
1. User edits content and clicks `Generate`.
2. UI sends payload to `POST /latex/render`.
3. UI shows progress state while compiling.
4. On success, UI loads `previewUrl` in embedded viewer.
5. UI enables download buttons (`PDF`, `TEX`, optional `LOG`).
6. On failure, UI shows `errorSummary` and line diagnostics.

## UI State Model
- `idle`
- `submitting`
- `compiling`
- `compiled`
- `failed`

## Minimal Payload Contract
- `userId`
- `documentType`
- `templateId`
- `latexSource`
- `meta` (optional)

## Error UX Rules
- Keep prior preview visible if last compile was successful.
- Show latest compile failure in a side panel.
- Highlight actionable line numbers from diagnostics.

## Download UX Rules
- Enable download only when artifact exists.
- Default primary action: `Download PDF`.
- Secondary actions: `Download TEX`, `Download LOG`.
