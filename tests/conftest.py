"""Test fixtures for file-memory tests."""

import json
from pathlib import Path

import pytest

from file_memory.store import MemoryStore


@pytest.fixture
def tmp_memory_dir(tmp_path: Path) -> Path:
    """Create a temporary memory directory."""
    memory_dir = tmp_path / "memory"
    memory_dir.mkdir()
    return memory_dir


@pytest.fixture
def memory_store(tmp_memory_dir: Path) -> MemoryStore:
    """Create a MemoryStore with a temporary directory."""
    return MemoryStore(base_dir=tmp_memory_dir)


@pytest.fixture
def sample_json_memory(tmp_memory_dir: Path) -> dict:
    """Create a sample JSON memory file."""
    data = {
        "metadata": {
            "key": "test_key",
            "format": "json",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "tags": ["test", "sample"],
        },
        "content": '{"name": "test", "value": 42}',
    }
    file_path = tmp_memory_dir / "test_key.json"
    file_path.write_text(json.dumps(data))
    return data
