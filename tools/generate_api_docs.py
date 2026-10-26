"""Generate docs/api-reference.md from the typed submodules.

Run from the repository root:

    python tools/generate_api_docs.py

The generated file is a quick method/endpoint index. Hand-written guides cover
authentication, leaderboards, and game IDs; this file keeps the surface area
easy to scan and easy to update.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMODULES = ROOT / "src" / "blockmango" / "submodules"
OUTPUT = ROOT / "docs" / "api-reference.md"


def extract_path(node: ast.AST) -> str:
    candidates: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            value = child.value
            if value.startswith("/") and "/" in value[1:]:
                candidates.append(value)
        elif isinstance(child, ast.JoinedStr):
            parts: list[str] = []
            for item in child.values:
                if isinstance(item, ast.Constant) and isinstance(item.value, str):
                    parts.append(item.value)
                elif isinstance(item, ast.FormattedValue):
                    parts.append("{" + ast.unparse(item.value) + "}")
            value = "".join(parts)
            if value.startswith("/"):
                candidates.append(value)
    return max(candidates, key=len) if candidates else ""


def short_doc(node: ast.AST) -> str:
    doc = ast.get_docstring(node) or ""
    return " ".join(doc.strip().split()).replace("|", "\\|")


def arguments(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    rendered = ast.unparse(node.args)
    if rendered.startswith("self, "):
        rendered = rendered[6:]
    elif rendered == "self":
        rendered = ""
    return rendered.replace("|", "\\|")


def render() -> str:
    lines = [
        "# API reference",
        "",
        "Generated from `src/blockmango/submodules/` by",
        "`python tools/generate_api_docs.py`. The hand-written guides are:",
        "",
        "- [api-overview.md](api-overview.md)",
        "- [authentication.md](authentication.md)",
        "- [leaderboards.md](leaderboards.md)",
        "- [games.md](games.md)",
        "",
        "Each row is a public method, its HTTP path when statically visible, and",
        "its short description. Methods that delegate to another module show `—`.",
        "`ExtendedAPI` is synchronous; use `account.async_request()` for async callers.",
        "",
    ]
    for path in sorted(SUBMODULES.glob("*.py")):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            doc = short_doc(node)
            lines.append(f"## `{node.name}`")
            if doc:
                lines.append("")
                lines.append(doc)
            lines.append("")
            lines.append("| Method | Endpoint | Description |")
            lines.append("| --- | --- | --- |")
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if item.name.startswith("_"):
                    continue
                endpoint = extract_path(item) or "—"
                prefix = "async " if isinstance(item, ast.AsyncFunctionDef) else ""
                method = f"`{prefix}{item.name}({arguments(item)})`"
                lines.append(f"| {method} | `{endpoint}` | {short_doc(item)} |")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(), encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
