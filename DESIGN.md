# File Memory for OpenCode - Design Document

## Overview

File Memory is a persistent storage solution for OpenCode that allows storing shared knowledge across sessions and projects. It's designed as a simple, file-based key-value store with support for JSON and Markdown formats.

## Goals

1. **Persistence**: Memories survive across OpenCode sessions
2. **Simplicity**: No database required, files are human-readable
3. **Flexibility**: Support both structured data (JSON) and notes (Markdown)
4. **Discoverability**: Tags and search for finding relevant memories
5. **Integration**: Seamless OpenCode skill and command support

## Architecture

### Storage Model

- **Directory**: `~/Documents/opencode/file_memory` (configurable)
- **File per Memory**: Each memory stored as `key.json` or `key.md`
- **Format**: JSON with schema versioning, Markdown with YAML frontmatter

### Schema Versioning

Current version: `1`

| Version | Format | Status |
|---------|--------|--------|
| 0 | Legacy | Read-only support |
| 1 | Current | Full support |

### Key Design Decisions

1. **One file per memory**: Simplifies management, enables git-friendly storage
2. **Sanitized filenames**: Keys are sanitized for filesystem safety
3. **Collision detection**: Prevents overwriting unrelated keys
4. **Frontmatter for Markdown**: Standard YAML frontmatter with metadata

## Data Models

### MemoryMetadata

```python
{
    "key": str,           # Original key (not sanitized)
    "format": str,        # "json" or "markdown"
    "created_at": datetime,
    "updated_at": datetime,
    "tags": list[str]
}
```

### MemoryEntry

```python
{
    "metadata": MemoryMetadata,
    "content": str       # JSON object as Python dict, or markdown string
}
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `store` | Store a new memory |
| `get` | Retrieve a memory |
| `list-memories` | List all memories |
| `update` | Update existing memory |
| `delete` | Delete a memory |
| `search` | Search by content |
| `list-tags` | List all tags |
| `init` | Initialize directory |

## Error Handling

| Exception | Use Case |
|-----------|----------|
| `MemoryStoreError` | General storage errors |
| `MemoryNotFoundError` | Key doesn't exist |
| `MemoryKeyError` | Invalid key or collision |
| `MemoryParseError` | Corrupted file |

## Future Considerations

- [ ] Add encryption for sensitive data
- [ ] Support for nested/hierarchical keys
- [ ] Export/import functionality
- [ ] Sync mechanism for multiple machines
- [ ] Web interface for manual editing

## Alternatives Considered

1. **SQLite**: More complex, requires additional dependency
2. **Redis**: Requires server, not persistent by default
3. **Flat JSON file**: Less human-readable, harder to edit manually
4. **Database**: Overkill for this use case

## References

- OpenCode Skills: https://opencode.ai/docs/skills/
- OpenCode Commands: https://opencode.ai/docs/commands/
