---
description: Capture information into memory with intelligent read-before-write workflow
agent: memory-capture
subtask: true
---

Capture information into file-memory with intelligent decision making.

This command invokes the memory-capture subagent which will:
1. Load the file-memory skill
2. Parse and classify the input (episodic/semantic/transient)
3. Search for related memories
4. Decide: create, update, skip, or reject
5. Optionally propagate updates to related memories (bounded)
6. Return the result to you

**Usage**:
```
/memory-capture <information to store>
```

Examples:
```
/memory-capture User prefers ruff for linting
/memory-capture Today I discovered a bug in the auth module - session tokens not being invalidated
/memory-capture Project convention: all tests go in tests/ directory
/memory-capture Current session goal: implement memory capture workflow
```

The subagent will:
- Reject transient thoughts that shouldn't be stored long-term
- Update existing memories if the new info supersedes them
- Create new memories for new information
- Reject if it cannot safely decide (with clear reason)

**Response states**:
- `captured`: New memory created
- `updated`: Existing memory revised
- `updated_with_propagation`: Updated plus related memories
- `deferred`: Some work queued for maintenance
- `skipped`: Valid but not stored (redundant)
- `rejected`: Cannot capture (will explain why)
