"""Tests for MemoryStore."""

import json

import pytest

from file_memory.store import MemoryNotFoundError, MemoryStore, MemoryStoreError


class TestMemoryStoreInit:
    """Tests for MemoryStore initialization."""

    def test_default_directory(self, tmp_memory_dir, monkeypatch):
        """Test default directory is set correctly."""
        monkeypatch.setattr("file_memory.store.get_memory_dir", lambda: tmp_memory_dir)
        store = MemoryStore()
        assert store.base_dir == tmp_memory_dir

    def test_custom_directory(self, tmp_memory_dir):
        """Test custom directory is used."""
        store = MemoryStore(base_dir=tmp_memory_dir)
        assert store.base_dir == tmp_memory_dir


class TestStoreMemory:
    """Tests for storing memories."""

    def test_store_json(self, memory_store):
        """Test storing a JSON memory."""
        entry = memory_store.store("test_key", {"name": "test", "value": 42})

        assert entry.metadata.key == "test_key"
        assert entry.metadata.format == "json"
        assert '"name": "test"' in entry.content
        assert '"value": 42' in entry.content

    def test_store_markdown(self, memory_store):
        """Test storing a markdown memory."""
        entry = memory_store.store("notes", "# Hello World", format="markdown")

        assert entry.metadata.key == "notes"
        assert entry.metadata.format == "markdown"
        assert entry.content == "# Hello World"

    def test_store_with_tags(self, memory_store):
        """Test storing with tags."""
        entry = memory_store.store("tagged", {"data": "value"}, tags=["tag1", "tag2"])

        assert entry.metadata.tags == ["tag1", "tag2"]

    def test_store_invalid_format(self, memory_store):
        """Test storing with invalid format raises error."""
        with pytest.raises(MemoryStoreError):
            memory_store.store("key", {"data": "value"}, format="xml")

    def test_store_json_requires_dict(self, memory_store):
        """Test JSON format requires dict content."""
        with pytest.raises(MemoryStoreError):
            memory_store.store("key", "not a dict", format="json")

    def test_store_creates_file(self, memory_store):
        """Test storing creates the file."""
        memory_store.store("my_key", {"data": "value"})

        file_path = memory_store.base_dir / "my_key.json"
        assert file_path.exists()


class TestGetMemory:
    """Tests for retrieving memories."""

    def test_get_json(self, memory_store):
        """Test retrieving a JSON memory."""
        memory_store.store("test_key", {"name": "test", "value": 42})

        entry = memory_store.get("test_key")

        assert entry.metadata.key == "test_key"
        assert entry.metadata.format == "json"

    def test_get_markdown(self, memory_store):
        """Test retrieving a markdown memory."""
        memory_store.store("notes", "# Hello", format="markdown")

        entry = memory_store.get("notes")

        assert entry.metadata.key == "notes"
        assert entry.metadata.format == "markdown"

    def test_get_nonexistent(self, memory_store):
        """Test retrieving non-existent key raises error."""
        with pytest.raises(MemoryNotFoundError):
            memory_store.get("does_not_exist")


class TestUpdateMemory:
    """Tests for updating memories."""

    def test_update_json(self, memory_store):
        """Test updating a JSON memory."""
        memory_store.store("test_key", {"value": 1})
        entry = memory_store.update("test_key", {"value": 2})

        assert json.loads(entry.content) == {"value": 2}

    def test_update_preserves_created_at(self, memory_store):
        """Test updating preserves creation timestamp."""
        memory_store.store("test_key", {"data": "original"})
        original = memory_store.get("test_key")
        created_at = original.metadata.created_at

        memory_store.update("test_key", {"data": "updated"})
        updated = memory_store.get("test_key")

        assert updated.metadata.created_at == created_at

    def test_update_nonexistent(self, memory_store):
        """Test updating non-existent key raises error."""
        with pytest.raises(MemoryNotFoundError):
            memory_store.update("does_not_exist", {"data": "value"})


class TestDeleteMemory:
    """Tests for deleting memories."""

    def test_delete_json(self, memory_store):
        """Test deleting a JSON memory."""
        memory_store.store("test_key", {"data": "value"})
        memory_store.delete("test_key")

        with pytest.raises(MemoryNotFoundError):
            memory_store.get("test_key")

    def test_delete_markdown(self, memory_store):
        """Test deleting a markdown memory."""
        memory_store.store("notes", "# Hello", format="markdown")
        memory_store.delete("notes")

        with pytest.raises(MemoryNotFoundError):
            memory_store.get("notes")

    def test_delete_nonexistent(self, memory_store):
        """Test deleting non-existent key raises error."""
        with pytest.raises(MemoryNotFoundError):
            memory_store.delete("does_not_exist")


class TestListMemories:
    """Tests for listing memories."""

    def test_list_empty(self, memory_store):
        """Test listing empty store returns nothing."""
        entries = list(memory_store.list())
        assert len(entries) == 0

    def test_list_multiple(self, memory_store):
        """Test listing multiple memories."""
        memory_store.store("key1", {"data": "1"})
        memory_store.store("key2", {"data": "2"})

        entries = list(memory_store.list())
        assert len(entries) == 2

    def test_list_by_tag(self, memory_store):
        """Test filtering by tag."""
        memory_store.store("tagged", {"data": "1"}, tags=["important"])
        memory_store.store("other", {"data": "2"}, tags=["other"])

        entries = list(memory_store.list(tag="important"))
        assert len(entries) == 1
        assert entries[0].metadata.key == "tagged"


class TestSearch:
    """Tests for searching memories."""

    def test_search_finds_match(self, memory_store):
        """Test search finds matching content."""
        memory_store.store("key1", {"data": "hello world"})

        results = list(memory_store.search("hello"))
        assert len(results) == 1

    def test_search_case_insensitive(self, memory_store):
        """Test search is case insensitive."""
        memory_store.store("key1", {"data": "HELLO"})

        results = list(memory_store.search("hello"))
        assert len(results) == 1


class TestTags:
    """Tests for tag functionality."""

    def test_tags_returns_all_tags(self, memory_store):
        """Test getting all unique tags."""
        memory_store.store("key1", {"data": "1"}, tags=["a", "b"])
        memory_store.store("key2", {"data": "2"}, tags=["b", "c"])

        tags = memory_store.tags()
        assert tags == {"a", "b", "c"}
