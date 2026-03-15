---
description: List all memories in file-memory
agent: general
---

List all stored memories in file-memory, optionally filtered by tag.

Run:
```
file-memory list-memories
file-memory list-memories --tag $1
file-memory list-memories --json
```

Replace:
- $1 = optional tag to filter by

Examples:
```
file-memory list-memories
file-memory list-memories --tag work
file-memory list-memories --json
```
