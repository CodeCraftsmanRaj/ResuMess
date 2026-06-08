# LaTeX Engine ↔ UI Contract

## Objective
Define a stable interface so UI and backend can ship independently.

## Render Request
`POST /latex/render`

### Request Body
- `userId` (string)
- `documentType` (`resume` | `cv` | `sop`)
- `templateId` (string, default `jakes`)
- `latexSource` (string)
- `meta` (optional object: `company`, `role`, `jdHash`)

### Success Response (200)
- `docId` (string)
- `status` (`compiled`)
- `previewUrl` (string)
- `downloads`:
  - `pdf`
  - `tex`
  - `log`

### Failure Response (422/500)
- `status` (`failed`)
- `errorSummary` (string)
- `errors[]`:
  - `line` (number | null)
  - `message` (string)
  - `severity` (`error` | `warning`)

## Preview API
`GET /latex/preview/{docId}`
- Returns embeddable PDF stream.

## Download API
`GET /latex/download/{docId}?type=pdf|tex|log`
- Returns selected artifact.

## UI Expectations
- Poll or subscribe for render status.
- Show compile diagnostics with line references.
- Keep previous successful preview until new compile succeeds.
- Offer direct download buttons for PDF and TEX.
