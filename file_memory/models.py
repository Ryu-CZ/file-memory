"""Data models for file-memory."""

from datetime import datetime

from pydantic import BaseModel, Field


class MemoryMetadata(BaseModel):
    """Metadata for a memory entry."""

    key: str
    format: str = "json"
    memory_type: str = "semantic"  # episodic, semantic, transient
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)


class MemoryEntry(BaseModel):
    """A complete memory entry with metadata and content."""

    metadata: MemoryMetadata
    content: str

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return self.model_dump(mode="json")
