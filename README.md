# File Memory for OpenCode

A persistent storage solution for OpenCode that allows sharing knowledge across sessions and projects. Store project progress, long-term goals, tool information, and more.

## Features

- **Persistent Storage**: Memories persist across OpenCode sessions
- **Dual Format Support**: Store as JSON or Markdown
- **Tag Organization**: Organize memories with tags
- **Full-text Search**: Search through all your memories
- **CLI & Python API**: Use via command line or import as a library
- **OpenCode Integration**: Built-in skill and commands for seamless OpenCode usage

## Quick Start

### Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/file-memory.git
cd file-memory

# Install in development mode
pip install -e ".[dev]"

# Or install globally (requires pipx or venv)
pipx install -e .
```

### Basic Usage

```bash
# Initialize (creates memory directory)
file-memory init

# Store a memory (JSON)
file-memory store project_progress '{"status": "in_progress", "goal": "build feature"}'

# Store a memory (Markdown)
file-memory store notes "# My Notes" --format markdown

# Store with tags
file-memory store my_key '{"data": "value"}' --tags project,important

# Store from file
file-memory store config --file /path/to/config.json

# Retrieve a memory
file-memory get project_progress

# Get as JSON (useful for scripts)
file-memory get project_progress --json

# List all memories
file-memory list-memories

# Filter by tag
file-memory list-memories --tag important

# Search memories
file-memory search "feature"

# List all tags
file-memory list-tags

# Update a memory
file-memory update project_progress '{"status": "done"}'

# Delete a memory
file-memory delete project_progress
```

## Configuration

### Environment Variables

```bash
# Override default memory directory
export FILE_MEMORY_DIR="/path/to/memories"
```

### CLI Option

```bash
file-memory --dir /custom/path get my_key
```

### Default Memory Location

```
~/Documents/opencode/file_memory
```

## Python API

```python
from file_memory import MemoryStore

# Create a store (uses default directory)
store = MemoryStore()

# Or use custom directory
from pathlib import Path
store = MemoryStore(base_dir=Path("/custom/path"))

# Store memories
store.store("project_x", {"status": "in_progress", "goal": "ship"}, tags=["work"])

# Retrieve
entry = store.get("project_x")
print(entry.content)

# List all
for entry in store.list():
    print(entry.metadata.key, entry.metadata.tags)

# Search
for entry in store.search("shipping"):
    print(entry.content)

# Update
store.update("project_x", {"status": "done"})

# Delete
store.delete("project_x")
```

## OpenCode Integration

This package includes built-in integration for OpenCode:

### Setup (Manual)

1. Symlink the skill and commands to your OpenCode config:

```bash
mkdir -p ~/.config/opencode/skills ~/.config/opencode/commands
ln -sf /path/to/file-memory/.opencode/skills/file-memory ~/.config/opencode/skills/
ln -sf /path/to/file-memory/.opencode/commands/*.md ~/.config/opencode/commands/
```

2. Ensure `file-memory` CLI is in your PATH:

```bash
ln -sf /path/to/file-memory/.venv/bin/file-memory ~/.local/bin/
```

### Usage in OpenCode

Once configured, you can use:

```bash
# In a bash block
file-memory store my_project '{"status": "working on auth"}'
file-memory get my_project
file-memory list-memories
file-memory search "auth"
```

Slash commands (if configured):
- `/memory-store` - Store a new memory
- `/memory-get` - Retrieve a memory
- `/memory-list` - List all memories
- `/memory-search` - Search memories

## Storage Format

### JSON Memory

```json
{
  "schema_version": 1,
  "metadata": {
    "key": "my_key",
    "format": "json",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "tags": ["work", "important"]
  },
  "content": {
    "status": "in_progress",
    "goal": "ship"
  }
}
```

### Markdown Memory

```markdown
---
schema_version: 1
key: notes
format: markdown
created_at: '2024-01-01T00:00:00'
updated_at: '2024-01-02T00:00:00'
tags:
- thoughts
- ideas
---

# My Notes

Content goes here...
```

## Use Cases

1. **Project Progress**: Track ongoing work across sessions
2. **Long-term Goals**: Remember what you want to achieve
3. **Tool Discovery**: Store info about tools you develop for testing
4. **Context Sharing**: Share information across different projects
5. **Knowledge Base**: Build a personal knowledge base

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=file_memory --cov-report=html

# Lint
ruff check .
ruff check --fix .

# Type check
mypy .
```

## License

MIT
