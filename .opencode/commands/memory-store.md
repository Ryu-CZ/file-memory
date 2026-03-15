---
description: DEPRECATED - Use /memory-recall instead
agent: general
---

**DEPRECATED**: This command is deprecated. Use `/memory-recall` instead.

---

Store a new memory in file-memory for persistent storage across sessions.

For new code, use `/memory-capture` which intelligently decides whether to create or update memories.

If you must use this directly:
```
file-memory store $1 '$2' --format $3 --tags $4 --type $5
```

Replace:
- $1 = memory key (e.g., `project_status`, `auth_feature`)
- $2 = content (JSON string or markdown text)
- $3 = format (json or markdown, default: json)
- $4 = tags (optional, comma-separated)
- $5 = memory type: episodic, semantic (default), or transient

Examples:
```
file-memory store project_status '{"status": "in_progress", "goal": "ship"}'
file-memory store notes '# Project Notes' --format markdown --tags ideas,planning
file-memory store config --file /path/to/config.json
```
