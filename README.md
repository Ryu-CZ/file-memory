# File Memory for OpenCode

A persistent storage solution for OpenCode that allows sharing knowledge across sessions and projects. Store project progress, long-term goals, tool information, and more.

## Features

- **Persistent Storage**: Memories persist across OpenCode sessions
- **Dual Format Support**: Store as JSON or Markdown
- **Tag Organization**: Organize memories with tags
- **Full-text Search**: Search through all your memories
- **CLI & Python API**: Use via command line or import as a library
- **OpenCode Integration**: Built-in skill and commands for seamless OpenCode usage

## Installation

### Quick Install

```bash
pip install file-memory
```

### Development Install

```bash
git clone https://github.com/yourusername/file-memory.git
cd file-memory
pip install -e ".[dev]"
```

## Usage

### CLI Commands

```bash
# Initialize the memory directory
file-memory init

# Store a memory (JSON)
file-memory store project_progress '{"status": "in_progress", "goal": "build feature"}'

# Store a memory (Markdown)
file-memory store notes "# My Notes" --format markdown

# Store with tags
file-memory store my_key '{"data": "value"}' --tags project,important

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

### Python API

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

## Default Memory Location

```
~/Documents/opencode/file_memory
```

## OpenCode Integration

This package includes built-in integration for OpenCode:

### Skill

Load the file-memory skill to let OpenCode know how to use this tool:

```
skill({ name: "file-memory" })
```

### Commands

Quick access slash commands are available:

- `/memory-store` - Store a new memory
- `/memory-get` - Retrieve a memory
- `/memory-list` - List all memories
- `/memory-search` - Search memories

## Use Cases

1. **Project Progress**: Track ongoing work across sessions
2. **Long-term Goals**: Remember what you want to achieve
3. **Tool Discovery**: Store info about tools you develop for testing
4. **Context Sharing**: Share context between different projects
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
