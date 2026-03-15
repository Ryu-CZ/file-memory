"""Core storage implementation for file-memory."""

import json
import logging
import re
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

from file_memory.config import ensure_memory_dir, get_memory_dir
from file_memory.models import MemoryEntry, MemoryMetadata

logger = logging.getLogger(__name__)


class MemoryStoreError(Exception):
    """Base exception for memory store errors."""

    pass


class MemoryNotFoundError(MemoryStoreError):
    """Raised when a memory entry is not found."""

    pass


class MemoryStore:
    """Main class for managing memory entries."""

    VALID_FORMATS = ("json", "markdown")

    def __init__(self, base_dir: Path | None = None):
        """Initialize the memory store.

        Args:
            base_dir: Optional custom directory for storing memories.
                     Defaults to ~/Documents/opencode/file_memory
        """
        self.base_dir = base_dir or get_memory_dir()
        self.base_dir = ensure_memory_dir(self.base_dir)

    def _get_file_path(self, key: str, format: str = "json") -> Path:
        """Get the file path for a memory key.

        Args:
            key: The memory key.
            format: The format extension (json or md).

        Returns:
            Path to the memory file.
        """
        safe_key = self._sanitize_key(key)
        ext = "json" if format == "json" else "md"
        return self.base_dir / f"{safe_key}.{ext}"

    def _sanitize_key(self, key: str) -> str:
        """Sanitize a key for use as a filename.

        Args:
            key: The key to sanitize.

        Returns:
            Sanitized key safe for filesystem use.
        """
        safe = re.sub(r"[^\w\-.]", "_", key)
        return safe[:200]

    def store(
        self,
        key: str,
        content: Any,
        format: str = "json",
        tags: list[str] | None = None,
    ) -> MemoryEntry:
        """Store a new memory entry.

        Args:
            key: Unique identifier for the memory.
            content: The content to store (dict for JSON, str for markdown).
            format: Format type ("json" or "markdown").
            tags: Optional list of tags.

        Returns:
            The created MemoryEntry.

        Raises:
            MemoryStoreError: If format is invalid.
        """
        if format not in self.VALID_FORMATS:
            raise MemoryStoreError(f"Invalid format: {format}. Must be one of {self.VALID_FORMATS}")

        if format == "json" and not isinstance(content, dict):
            raise MemoryStoreError("JSON format requires dict content")

        if format == "markdown" and not isinstance(content, str):
            raise MemoryStoreError("Markdown format requires string content")

        file_path = self._get_file_path(key, format)

        now = datetime.now()
        content_str = json.dumps(content, indent=2) if format == "json" else str(content)

        metadata = MemoryMetadata(
            key=key,
            format=format,
            created_at=now,
            updated_at=now,
            tags=tags or [],
        )

        entry = MemoryEntry(metadata=metadata, content=content_str)

        if format == "json":
            data = {
                "metadata": metadata.model_dump(),
                "content": content_str,
            }
            file_path.write_text(json.dumps(data, indent=2, default=str))
        else:
            frontmatter = json.dumps(metadata.model_dump(), default=str)
            file_path.write_text(f"---\n{frontmatter}\n---\n\n{content_str}")

        logger.info(f"Stored memory: {key} at {file_path}")
        return entry

    def get(self, key: str) -> MemoryEntry:
        """Retrieve a memory entry by key.

        Args:
            key: The memory key to retrieve.

        Returns:
            The MemoryEntry.

        Raises:
            MemoryNotFoundError: If the memory doesn't exist.
        """
        for fmt in self.VALID_FORMATS:
            file_path = self._get_file_path(key, fmt)
            if file_path.exists():
                return self._read_entry(file_path, fmt)

        raise MemoryNotFoundError(f"Memory '{key}' not found")

    def _read_entry(self, file_path: Path, format: str) -> MemoryEntry:
        """Read a memory entry from disk.

        Args:
            file_path: Path to the memory file.
            format: Format of the file.

        Returns:
            The MemoryEntry.
        """
        content = file_path.read_text()

        if format == "json":
            data = json.loads(content)
            return MemoryEntry(
                metadata=MemoryMetadata(**data["metadata"]),
                content=data["content"],
            )
        else:
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = json.loads(parts[1].strip())
                    markdown_content = parts[2].strip()
                    return MemoryEntry(
                        metadata=MemoryMetadata(**frontmatter),
                        content=markdown_content,
                    )

            return MemoryEntry(
                metadata=MemoryMetadata(key=file_path.stem, format="markdown"),
                content=content,
            )

    def update(
        self,
        key: str,
        content: Any,
        tags: list[str] | None = None,
    ) -> MemoryEntry:
        """Update an existing memory entry.

        Args:
            key: The memory key to update.
            content: The new content.
            tags: Optional new tags (keeps existing if not provided).

        Returns:
            The updated MemoryEntry.

        Raises:
            MemoryNotFoundError: If the memory doesn't exist.
        """
        existing = self.get(key)
        file_path = self._get_file_path(key, existing.metadata.format)

        now = datetime.now()

        if existing.metadata.format == "json":
            if not isinstance(content, dict):
                raise MemoryStoreError("JSON format requires dict content")
            content_str = json.dumps(content, indent=2)
        else:
            if not isinstance(content, str):
                raise MemoryStoreError("Markdown format requires string content")
            content_str = str(content)

        new_tags = tags if tags is not None else existing.metadata.tags

        metadata = MemoryMetadata(
            key=key,
            format=existing.metadata.format,
            created_at=existing.metadata.created_at,
            updated_at=now,
            tags=new_tags,
        )

        entry = MemoryEntry(metadata=metadata, content=content_str)

        if metadata.format == "json":
            data = {
                "metadata": metadata.model_dump(),
                "content": content_str,
            }
            file_path.write_text(json.dumps(data, indent=2, default=str))
        else:
            frontmatter = json.dumps(metadata.model_dump(), default=str)
            file_path.write_text(f"---\n{frontmatter}\n---\n\n{content_str}")

        logger.info(f"Updated memory: {key}")
        return entry

    def delete(self, key: str) -> None:
        """Delete a memory entry.

        Args:
            key: The memory key to delete.

        Raises:
            MemoryNotFoundError: If the memory doesn't exist.
        """
        for fmt in self.VALID_FORMATS:
            file_path = self._get_file_path(key, fmt)
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted memory: {key}")
                return

        raise MemoryNotFoundError(f"Memory '{key}' not found")

    def list(self, tag: str | None = None) -> Iterator[MemoryEntry]:
        """List all memory entries.

        Args:
            tag: Optional tag to filter by.

        Yields:
            MemoryEntry objects.
        """
        for file_path in self.base_dir.iterdir():
            if file_path.is_file() and file_path.suffix in (".json", ".md"):
                try:
                    fmt = "json" if file_path.suffix == ".json" else "markdown"
                    entry = self._read_entry(file_path, fmt)
                    if tag is None or tag in entry.metadata.tags:
                        yield entry
                except Exception as e:
                    logger.warning(f"Failed to read {file_path}: {e}")

    def search(self, query: str) -> Iterator[MemoryEntry]:
        """Search memory entries by content.

        Args:
            query: The search query.

        Yields:
            Matching MemoryEntry objects.
        """
        query_lower = query.lower()
        for entry in self.list():
            if query_lower in entry.content.lower():
                yield entry

    def tags(self) -> set[str]:
        """Get all unique tags across all memories.

        Returns:
            Set of tag strings.
        """
        all_tags: set[str] = set()
        for entry in self.list():
            all_tags.update(entry.metadata.tags)
        return all_tags
