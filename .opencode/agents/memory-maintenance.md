---
name: memory-maintenance
description: Offline memory consolidation agent - processes deferred work, resolves conflicts, abstracts episodes (NOT YET IMPLEMENTED)
mode: subagent
hidden: true
---

## Status: NOT IMPLEMENTED

This agent is a placeholder for future "dream mode" functionality.

### Planned Features

**Responsibilities:**
- Process `~maintenance_pending` memories from capture phase
- Resolve contradictions across larger memory graph
- Abstract repeated episodes into semantic memories
- Deduplicate similar memories
- Reindex and optimize memory structure
- Clean up stale references

**Trigger conditions:**
- Manual invocation: `/memory-maintenance`
- Automatic: After N captures or time threshold (future)

**Budget:**
- No hard limits (offline, unbounded)
- Should run in background as subtask

### Current State

For now, use `memory-capture` with bounded propagation. Deferred work accumulates in `~maintenance_pending` memories.

### Example Deferred Items

```
~maintenance_pending:
  - action: update_related
    target: preference_test_framework
    reason: cascade from session_2026-03-15
    status: pending
  - action: resolve_conflict
    memories: [fact_about_foo, fact_about_bar]
    reason: contradictory claims about X
    status: pending
```

### Implementation TODO

When implementing:
1. Load all `~maintenance_pending` memories
2. Process each item with full graph access
3. Use higher confidence thresholds than capture
4. Create audit trail of changes made
5. Clear pending items when resolved
