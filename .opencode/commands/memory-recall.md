---
description: Recall memories - find and summarize relevant stored memories
agent: memory-recall
subtask: true
---

Recall relevant memories from file-memory.

This command invokes the memory-recall subagent which will:
1. Load the file-memory skill
2. Search for relevant memories
3. Return compact summaries to you

**Usage**:
```
/memory-recall <query or question>
```

Examples:
```
/memory-recall What was I working on last session?
/memory-recall user preferences
/memory-recall testing conventions for this project
/memory-recall Find all memories about auth
```

The subagent will search memories and return relevant results. If no memories are found, it will explicitly say so.
