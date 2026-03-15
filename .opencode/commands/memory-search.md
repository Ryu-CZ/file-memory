---
description: Search memories in file-memory
agent: general
---

Search through all stored memories in file-memory.

Run:
```
file-memory search '$1'
file-memory search '$1' --json
```

Replace:
- $1 = search query (matches content)

Examples:
```
file-memory search "project"
file-memory search "OAuth" --json
```
