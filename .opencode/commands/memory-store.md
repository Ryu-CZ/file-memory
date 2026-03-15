---
description: Store a memory in file-memory
agent: general
---

Store a new memory in file-memory for persistent storage across sessions.

Run:
```
file-memory store $1 '$2' --format $3 --tags $4
```

Replace:
- $1 = memory key (e.g., `project_status`, `auth_feature`)
- $2 = content (JSON string or markdown text)
- $3 = format (json or markdown, default: json)
- $4 = tags (optional, comma-separated)

Examples:
```
file-memory store project_status '{"status": "in_progress", "goal": "ship"}'
file-memory store notes '# Project Notes' --format markdown --tags ideas,planning
file-memory store config --file /path/to/config.json
```
