# UI Playground

A browser-testable frontend for manual flow checks.

## Run
From project root:

- `uv run python -m http.server 5500 -d ui`

Then open:

- `http://localhost:5500`

## What to test
- Click **Mock Success** and verify preview + downloads state.
- Click **Mock Failure** and verify diagnostics rendering.
- Set API base and click **Generate** to call `POST /latex/render`.

This UI follows the contract in [docs/latex-ui-contract.md](../docs/latex-ui-contract.md).
