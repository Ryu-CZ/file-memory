---
description: Run memory maintenance - consolidate memories, resolve conflicts, process deferred work
agent: memory-maintenance
subtask: true
---

Run offline memory consolidation.

This command invokes the memory-maintenance subagent which will:
1. Check for pending maintenance items in `~maintenance_pending`
2. Process deferred updates from memory-capture
3. Resolve larger conflicts
4. Optionally consolidate repeated episodes into semantic memories
5. Clean up processed items

**Usage**:
```
/memory-maintenance
```

This is "dream mode" - use it when:
- You have deferred work from capture phase
- Memory conflicts need resolution
- You want to consolidate episodic memories

The agent has unlimited budget (unlike capture's bounded propagation).
