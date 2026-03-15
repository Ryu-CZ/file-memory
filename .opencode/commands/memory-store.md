---
description: Store a memory in file-memory
agent: general
---

Store a new memory in file-memory for persistent storage across sessions.

The memory key should be descriptive (e.g., `project_x_progress`, `auth_feature_goals`).
Use JSON format for structured data, Markdown for notes.

Run: `file-memory store $1 '$2' --format $3 --tags $4`

Replace:
- $1 = memory key (e.g., `my_key`)
- $2 = content (JSON string or markdown)
- $3 = format (json or markdown, default: json)
- $4 = tags (optional, comma-separated)

Example: `file-memory store project_status '{"status": "in_progress"}' --tags work`
