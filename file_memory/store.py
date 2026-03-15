"""Core storage implementation for file-memory."""

import json
import logging
import re
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from file_memory.config import ensure_memory_dir, get_memory_dir
from file_memory.models import MemoryEntry, MemoryMetadata

logger = logging.getLogger(__name__)

CURRENT_SCHEMA_VERSION = 1


class MemoryStoreError(Exception):
    """Base exception for memory store errors."""

    pass


class MemoryNotFoundError(MemoryStoreError):
    """Raised when a memory entry is not found."""

    pass


class MemoryKeyError(MemoryStoreError):
    """Raised for invalid or conflicting memory keys."""

    pass


class MemoryParseError(MemoryStoreError):
    """Raised when a memory file cannot be parsed."""

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

        Raises:
            MemoryKeyError: If key is empty after sanitization.
        """
        if not key or not key.strip():
            raise MemoryKeyError("Key cannot be empty")

        safe = re.sub(r"[^\w\-.]", "_", key)
        safe = safe[:200]

        if not safe:
            raise MemoryKeyError(f"Key '{key}' produces invalid filename")

        return safe

    def _check_key_collision(self, key: str, format: str, existing_key: str | None = None) -> None:
        """Check for key collisions after sanitization.

        Args:
            key: Original key provided by user.
            format: Format being stored.
            existing_key: If updating, the key that currently exists.

        Raises:
            MemoryKeyError: If sanitized key collides with existing file.
        """
        safe_key = self._sanitize_key(key)

        for fmt in self.VALID_FORMATS:
            file_path = self.base_dir / f"{safe_key}.{'json' if fmt == 'json' else 'md'}"
            if file_path.exists():
                if existing_key and self._sanitize_key(existing_key) == safe_key:
                    continue
                raise MemoryKeyError(
                    f"Key '{key}' sanitizes to '{safe_key}' which collides with existing memory"
                )

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
            MemoryKeyError: If key is invalid or collides.
        """
        if format not in self.VALID_FORMATS:
            raise MemoryStoreError(f"Invalid format: {format}. Must be one of {self.VALID_FORMATS}")

        if format == "json" and not isinstance(content, dict):
            raise MemoryStoreError("JSON format requires dict content")

        if format == "markdown" and not isinstance(content, str):
            raise MemoryStoreError("Markdown format requires string content")

        self._check_key_collision(key, format)

        now = datetime.now()

        metadata = MemoryMetadata(
            key=key,
            format=format,
            created_at=now,
            updated_at=now,
            tags=tags or [],
        )

        file_path = self._get_file_path(key, format)

        if format == "json":
            data = {
                "schema_version": CURRENT_SCHEMA_VERSION,
                "metadata": metadata.model_dump(mode="json"),
                "content": content,
            }
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
            content_str = json.dumps(content, indent=2)
        else:
            frontmatter = {
                "schema_version": CURRENT_SCHEMA_VERSION,
                **metadata.model_dump(mode="json"),
            }
            with open(file_path, "w") as f:
                f.write("---\n")
                yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
                f.write("---\n\n")
                f.write(str(content))

            content_str = str(content)

        entry = MemoryEntry(metadata=metadata, content=content_str)

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
        safe_key = self._sanitize_key(key)

        for fmt in self.VALID_FORMATS:
            file_path = self.base_dir / f"{safe_key}.{'json' if fmt == 'json' else 'md'}"
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

        Raises:
            MemoryParseError: If the file cannot be parsed.
        """
        try:
            content = file_path.read_text()
        except Exception as e:
            raise MemoryParseError(f"Cannot read {file_path}: {e}") from e

        if format == "json":
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                raise MemoryParseError(f"Invalid JSON in {file_path}: {e}") from e

            if not isinstance(data, dict):
                raise MemoryParseError(f"Invalid JSON structure in {file_path}")

            schema_version = data.get("schema_version", 0)

            if schema_version == 0:
                return self._read_legacy_json(file_path, data)
            elif schema_version == 1:
                metadata = MemoryMetadata(**data["metadata"])
                content_value = data["content"]
                content_str = json.dumps(content_value, indent=2)
                return MemoryEntry(metadata=metadata, content=content_str)
            else:
                raise MemoryParseError(f"Unknown schema version {schema_version} in {file_path}")
        else:
            return self._read_markdown(file_path, content)

    def _read_legacy_json(self, file_path: Path, data: dict) -> MemoryEntry:
        """Read legacy JSON format (schema v0 - content as string).

        Args:
            file_path: Path to the file.
            data: Parsed JSON data.

        Returns:
            The MemoryEntry.
        """
        metadata = MemoryMetadata(**data["metadata"])

        content_str = data.get("content", "")
        if isinstance(content_str, str):
            try:
                content_value = json.loads(content_str)
            except json.JSONDecodeError:
                content_value = {"raw": content_str}
        else:
            content_value = content_str

        normalized_content = json.dumps(content_value, indent=2)

        return MemoryEntry(metadata=metadata, content=normalized_content)

    def _read_markdown(self, file_path: Path, content: str) -> MemoryEntry:
        """Read a markdown memory entry.

        Supports both new YAML frontmatter and legacy JSON frontmatter.

        Args:
            file_path: Path to the file.
            content: File content.

        Returns:
            The MemoryEntry.
        """
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1].strip()
                markdown_content = parts[2].strip()

                try:
                    frontmatter = yaml.safe_load(frontmatter_str)
                except yaml.YAMLError:
                    try:
                        frontmatter = json.loads(frontmatter_str)
                    except json.JSONDecodeError:
                        frontmatter = {"key": file_path.stem, "format": "markdown"}

                schema_version = frontmatter.get("schema_version", 0)

                if schema_version == 0:
                    metadata = MemoryMetadata(**frontmatter)
                else:
                    metadata = MemoryMetadata(
                        key=frontmatter.get("key", file_path.stem),
                        format=frontmatter.get("format", "markdown"),
                        created_at=frontmatter.get("created_at", datetime.now()),
                        updated_at=frontmatter.get("updated_at", datetime.now()),
                        tags=frontmatter.get("tags", []),
                    )

                return MemoryEntry(metadata=metadata, content=markdown_content)

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
            MemoryKeyError: If key collision is detected.
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

        if metadata.format == "json":
            data = {
                "schema_version": CURRENT_SCHEMA_VERSION,
                "metadata": metadata.model_dump(mode="json"),
                "content": content,
            }
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
        else:
            frontmatter = {
                "schema_version": CURRENT_SCHEMA_VERSION,
                **metadata.model_dump(mode="json"),
            }
            with open(file_path, "w") as f:
                f.write("---\n")
                yaml.dump(frontmatter, f, default_flow_style=False, sort_keys=False)
                f.write("---\n\n")
                f.write(content_str)

        entry = MemoryEntry(metadata=metadata, content=content_str)

        logger.info(f"Updated memory: {key}")
        return entry

    def delete(self, key: str) -> None:
        """Delete a memory entry.

        Args:
            key: The memory key to delete.

        Raises:
            MemoryNotFoundError: If the memory doesn't exist.
        """
        safe_key = self._sanitize_key(key)

        for fmt in self.VALID_FORMATS:
            file_path = self.base_dir / f"{safe_key}.{'json' if fmt == 'json' else 'md'}"
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
            MemoryEntry objects in sorted order by key.
        """
        entries: list[MemoryEntry] = []

        for file_path in sorted(self.base_dir.iterdir()):
            if file_path.is_file() and file_path.suffix in (".json", ".md"):
                fmt = "json" if file_path.suffix == ".json" else "markdown"
                try:
                    entry = self._read_entry(file_path, fmt)
                    if tag is None or tag in entry.metadata.tags:
                        entries.append(entry)
                except MemoryParseError as e:
                    logger.warning(f"Skipping invalid memory {file_path}: {e}")

        yield from sorted(entries, key=lambda e: e.metadata.key)

    def search(self, query: str) -> Iterator[MemoryEntry]:
        """Search memory entries by content.

        Args:
            query: The search query.

        Yields:
            Matching MemoryEntry objects in sorted order by key.
        """
        query_lower = query.lower()
        results = []

        for entry in self.list():
            if query_lower in entry.content.lower():
                results.append(entry)

        yield from sorted(results, key=lambda e: e.metadata.key)

    def tags(self) -> set[str]:
        """Get all unique tags across all memories.

        Returns:
            Sorted set of tag strings.
        """
        all_tags: set[str] = set()
        for entry in self.list():
            all_tags.update(entry.metadata.tags)
        return all_tags
