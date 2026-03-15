---
description: Direct store - write a memory with exact key (manual access)
agent: general
---

Direct memory storage - writes exactly what you specify.

**Usage**:
```
/mem-store <key> <content>
/mem-store <key> --file /path/to/content.json
```

This is a direct/manual command - no intelligent classification or conflict detection. Use `/memory-capture` for intelligent read-before-write workflow.

Examples:
```
/mem-store project_status '{"status": "in_progress"}'
/mem-store notes '# My Notes' --format markdown
```

**Options**:
- `--format json|markdown` (default: json)
- `--tags tag1,tag2`
- `--type episodic|semantic|transient`
- `--file /path/to/content`
