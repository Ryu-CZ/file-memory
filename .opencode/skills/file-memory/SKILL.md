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
- **Knowledge Base**: Store information you want to reference later

## Storage Location

Default: `~/Documents/opencode/file_memory`

You can override with:
- `--dir` CLI option
- `FILE_MEMORY_DIR` environment variable

## Available Commands

### Store a Memory

```bash
file-memory store <key> '<json_or_markdown>' --format json|markdown --tags tag1,tag2
```

Examples:
```bash
file-memory store project_x '{"status": "in_progress", "goal": "ship feature"}'
file-memory store notes '# My Notes' --format markdown --tags thoughts,ideas
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
```

### Search

```bash
file-memory search <query>
```

### Update

```bash
file-memory update <key> '<new_content>'
```

### Delete

```bash
file-memory delete <key>
```

### List Tags

```bash
file-memory list-tags
```

## How to Use Me

### In Conversation

When the user mentions storing something for later, remembering progress, or referencing previous work:

1. Use `file-memory store <key> <value>` to save information
2. Use `file-memory get <key>` to retrieve it
3. Use `file-memory list-memories` to see all stored memories

### Example Prompts

User: "Remember I'm working on the authentication feature"
→ Store: `file-memory store auth_feature '{"status": "in_progress", "task": "authentication", "goal": "add OAuth"}'`

User: "What was I working on last time?"
→ Run: `file-memory list-memories`

User: "Find my notes about the API"
→ Run: `file-memory search API`

## Best Practices

1. **Use descriptive keys**: `project_name_feature` instead of `x`
2. **Add tags**: Helps organize and filter memories
3. **Use JSON for structured data**: Easy to parse and update
4. **Use Markdown for notes**: Human-readable, great for long text

## Output Format

When retrieving memories with `--json`, the output is:

```json
{
  "metadata": {
    "key": "my_key",
    "format": "json",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "tags": ["work", "important"]
  },
  "content": "{...}"
}
```

## Notes

- Memories persist indefinitely until deleted
- Each memory is stored as a separate file (key.json or key.md)
- OpenCode can discover this skill automatically
- You can load this skill using the `skill` tool
