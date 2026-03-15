"""Configuration management for file-memory."""

import os
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / "Documents" / "opencode" / "file_memory"


def get_default_memory_dir() -> Path:
    """Get the default memory directory."""
    return DEFAULT_MEMORY_DIR


def get_memory_dir(env_override: str | None = None) -> Path:
    """Get the memory directory, optionally from environment variable."""
    if env_override:
        return Path(env_override)
    env_dir = os.environ.get("FILE_MEMORY_DIR")
    if env_dir:
        return Path(env_dir)
    return get_default_memory_dir()


def ensure_memory_dir(path: Path | None = None) -> Path:
    """Ensure the memory directory exists."""
    memory_dir = path or get_memory_dir()
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir
