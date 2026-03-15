# AGENTS.md - File Memory for OpenCode

## Project Overview

This project implements a file memory feature for OpenCode that stores shared knowledge in `~/Documents/opencode/file_memory` (project progress, long-term goals, tools info).

- **Language**: Python 3.10+
- **Storage**: JSON or Markdown

---

## Build, Lint, and Test Commands

### Run
```bash
python -m file_memory
python main.py
```

### Lint & Type Check
```bash
ruff check .
ruff check --fix .
ruff format .
mypy .
```

### Tests
```bash
pytest                    # all tests
pytest tests/test_memory.py           # single file
pytest tests/test_memory.py::test_store_memory  # single test
pytest -k "test_store"    # pattern match
pytest -v                 # verbose
pytest --cov=file_memory --cov-report=html  # coverage
```

### Dev Setup
```bash
pip install -e .
pip install -r requirements-dev.txt
pre-commit install
```

---

## Code Style

### Imports (in order)
1. Standard library
2. Third-party
3. Local application

```python
import json
import os
from pathlib import Path
from typing import Any

import click
from pydantic import BaseModel

from file_memory import MemoryStore
```

**Avoid**: wildcard imports, relative imports, multiple items on one line.

### Formatting
- Max 100 chars per line
- 4 spaces (no tabs)
- Two blank lines between top-level defs, one between functions

### Types
- Always use type hints
- Use `Optional[X]` not `X | None`
- Use `dict[str, Any]` for generic dicts (Python 3.10+)

### Naming
| Element | Convention | Example |
|---------|------------|---------|
| Functions | snake_case | `store_memory` |
| Classes | PascalCase | `MemoryStore` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_MEMORY_DIR` |
| Private methods | _snake_case | `_validate_path` |
| Files | snake_case.py | `memory_store.py` |

### Error Handling
- Use custom exceptions for domain errors
- Catch specific exceptions, not broad `Exception`
- Include context in error messages
- Use `logging` for non-fatal errors

```python
class MemoryError(Exception): pass
class MemoryNotFoundError(MemoryError): pass

def load_memory(key: str) -> dict[str, Any]:
    try:
        with open(_get_path(key)) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise MemoryNotFoundError(f"Memory '{key}' not found") from e
```

### Testing
- Use `pytest`
- Test files: `tests/test_<module>.py`
- Test functions: `test_<func>_<expected>`
- Follow Arrange-Act-Assert

```python
def test_store_creates_file(tmp_path):
    store = MemoryStore(base_dir=tmp_path)
    store.store("test_key", {"data": "value"})
    assert (tmp_path / "test_key.json").exists()
```

### Logging
- Use `logging.getLogger(__name__)`
- Appropriate levels: DEBUG, INFO, WARNING, ERROR

### Docstrings
- Use Google-style or NumPy-style consistently
- Document public APIs

---

## Project Structure

```
file_memory/
├── file_memory/
│   ├── __init__.py
│   ├── memory_store.py
│   ├── models.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_memory_store.py
├── pyproject.toml
└── README.md
```

---

## Configuration
- Use `pyproject.toml` for project metadata and tool config
- Configure Ruff and pytest in `pyproject.toml`

---

## Version Control
- Atomic commits with meaningful messages
- Run lint/tests before committing
