---
name: file-memory
description: Persistent memory storage for OpenCode - store project progress, goals, tool info across sessions
license: MIT
compatibility: opencode
metadata:
  audience: users
  use_cases: project-progress,long-term-goals,tool-discovery,context-sharing
---

## What I Am

I am file-memory, a persistent storage tool for OpenCode that stores knowledge in files that persist across all your coding sessions and projects. Think of me as your long-term memory that survives between conversations.

## When to Use Me

Use file-memory when you need to:

- **Track Project Progress**: Remember what you were working on in previous sessions
- **Store Long-term Goals**: Keep track of objectives you want to achieve
- **Tool Discovery**: Remember tools the user develops for you to test
- **Context Sharing**: Share information across different projects
- **Knowledge Base**: Build a personal knowledge base

## Storage Location

Default: `~/Documents/opencode/file_memory`

You can override with:
- `--dir` CLI option
- `FILE_MEMORY_DIR` environment variable

## Available CLI Commands

### Store a Memory

```bash
file-memory store <key> '<json_or_markdown>' --format json|markdown --tags tag1,tag2
# Or from file:
file-memory store <key> --file /path/to/content.json --format json
```

Examples:
```bash
file-memory store project_x '{"status": "in_progress", "goal": "ship feature"}'
file-memory store notes '# My Notes' --format markdown --tags thoughts,ideas
file-memory store config --file config.json
```

### Get a Memory

```bash
file-memory get <key>
file-memory get <key> --json  # JSON output for parsing
```

### List Memories

```bash
file-memory list-memories
file-memory list-memories --tag work  # Filter by tag
file-memory list-memories --json  # JSON output
```

### Search

```bash
file-memory search <query>
file-memory search <query> --json
```

### Update

```bash
file-memory update <key> '<new_content>'
file-memory update <key> --file /path/to/new_content.json
```

### Delete

```bash
file-memory delete <key>
```

### List Tags

```bash
file-memory list-tags
file-memory list-tags --json
```

## How to Use Me in OpenCode

### Direct CLI Usage

Simply run the `file-memory` command in a bash block:

```
file-memory store project_progress '{"status": "working on auth", "goal": "ship OAuth"}'
file-memory get project_progress
file-memory list-memories
file-memory search "OAuth"
```

### Slash Commands

Available commands (if configured):
- `/memory-store` - Store a new memory
- `/memory-get` - Retrieve a memory  
- `/memory-list` - List all memories
- `/memory-search` - Search memories

## Best Practices

1. **Use descriptive keys**: `project_name_feature` instead of `x`
2. **Add tags**: Helps organize and filter memories
3. **Use JSON for structured data**: Easy to parse and update
4. **Use Markdown for notes**: Human-readable, great for long text

## Output Format

When retrieving memories with `--json`, the output follows this schema:

```json
{
  "metadata": {
    "key": "my_key",
    "format": "json",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "tags": ["work", "important"]
  },
  "content": {...}
}
```

## Notes

- Memories persist indefinitely until deleted
- Each memory is stored as a separate file (key.json or key.md)
- Schema version is tracked for future compatibility
- Key collisions are detected and prevented
