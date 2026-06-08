from pathlib import Path


def test_versioning_module_exists_or_is_planned() -> None:
    """Guardrail placeholder: fails only if there is no versioning implementation or plan.

    This keeps CI meaningful while versioning code is under development.
    """
    candidates = [
        Path("src/resumess/versioning.py"),
        Path("src/resumess/versioning/__init__.py"),
        Path("docs/feature-versioning.md"),
    ]
    assert any(path.exists() for path in candidates), (
        "Versioning implementation/plan not found. "
        "Add versioning module or docs/feature-versioning.md before merging."
    )
