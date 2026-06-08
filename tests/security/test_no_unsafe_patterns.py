from pathlib import Path

DANGEROUS_PATTERNS = [
    "eval(",
    "exec(",
    "pickle.loads(",
    "yaml.load(",
    "subprocess.Popen(",
    "os.system(",
]


def test_no_obvious_unsafe_patterns_in_source() -> None:
    src_root = Path("src")
    if not src_root.exists():
        return

    violations: list[str] = []
    for py_file in src_root.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        for pattern in DANGEROUS_PATTERNS:
            if pattern in content:
                violations.append(f"{py_file}: contains `{pattern}`")

    assert not violations, "\n".join(violations)
