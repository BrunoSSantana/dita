# Conventions

## Python

- **Version**: 3.11+
- **Type hints**: required on all public functions and methods
- **Data structures**: use `dataclasses` or `TypedDict` at layer boundaries — no untyped dicts
- **Exceptions**: define in `src/core/exceptions.py`; never swallow silently
- **Logging**: `import logging` — no `print()` for debug output
- **Formatting**: `black` (line length 88) + `isort`
- **Linting**: `ruff`

```python
# good
def get_document(doc_id: str) -> Document:
    ...

# bad — no type hints, raw dict return
def get_document(doc_id):
    return {"id": doc_id}
```

## pywebview API Methods

- Must return JSON-serializable types (`dict`, `list`, `str`, `int`, `float`, `bool`, `None`)
- Wrap errors in a standard envelope — never raise uncaught exceptions to JS:

```python
# standard response envelope
{"ok": True, "data": ...}
{"ok": False, "error": "human-readable message"}
```

## Frontend (JS)

- All Python calls go through `window.pywebview.api.*`
- Calls are async — always `await` or use `.then()`
- No direct DOM manipulation from inline `<script>` — keep JS in `src/ui/js/`

## Tooling

| Tool | Purpose | Command |
|---|---|---|
| uv | dependency management | `uv add <pkg>` |
| black | formatting | `black src/ tests/` |
| isort | import sorting | `isort src/ tests/` |
| ruff | linting | `ruff check src/` |
| pytest | testing | `pytest tests/` |

## Testing Rules

- Unit tests: `tests/unit/` — import from `src/core/` only
- No webview instance in unit tests
- Name test files `test_<module>.py`
- One assertion per logical scenario (multiple asserts per test only when they form one logical check)
