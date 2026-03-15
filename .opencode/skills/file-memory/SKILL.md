---
name: file-memory
description: Persistent memory storage for OpenCode with cognitively-inspired workflow
license: MIT
compatibility: opencode
metadata:
  audience: agents
  use_cases: project-progress,long-term-goals,tool-discovery,context-sharing
---

## What I Am

I am file-memory, a persistent storage tool for OpenCode that stores knowledge in files that persist across all your coding sessions and projects. I provide both a simple storage layer AND a workflow contract for intelligent memory agents.

## Memory Model

### Memory Types

**Episodic Memory**
- Concrete events, sessions, decisions, failures, discoveries
- Dated, context-rich records
- Typically created as new records
- Example: "2026-03-15: Discovered ruff check B904 issue in cli.py"

**Semantic Memory**
- Stable facts, preferences, conventions, user habits, project truths
- Long-lived, updated rather than recreated
- Example: "user_prefers: test_dir=tests/, always_run_lint=true"

**Transient Memory**
- Should NOT be stored long-term
- Working context, temporary notes, in-progress thoughts
- Example: "current thought: should I refactor X?"

### Memory Lifecycle

1. **Encoding**: Parse input, classify as episodic/semantic/transient
2. **Retrieval**: Find related memories before any write
3. **Reconciliation**: Compare new info with existing, decide action
4. **Storage**: Create, update, or skip
5. **Propagation**: Optionally update related memories (bounded)

## Workflow Rules

### For Recall (Read-Only)

1. Always use `list-memories`, `list-tags`, `search`, `get` to retrieve
2. Rank results by relevance, recency, and confidence
3. Return compact summaries to parent, not raw dumps
4. If no relevant memories found, return explicit `none_found`

### For Capture (Read-Before-Write - MANDATORY)

**NEVER write without searching first.** This is the core rule.

#### Capture Pipeline

1. **Parse**: Extract key entities, claims, time references from input
2. **Classify**: Is this episodic? semantic? transient (skip)?
3. **Retrieve**: Search for related memories using:
   - Exact key match
   - Key similarity
   - Tag overlap
   - Content similarity
   - Entity/ topic overlap
4. **Decide**: Choose one action:
   - `create`: New memory, no close related exists
   - `update`: Existing memory needs revision (confidence threshold: 0.7)
   - `merge`: Combine with existing semantic record
   - `skip`: Valid but redundant/low-value
   - `reject`: Cannot safely capture (see rejection reasons below)
5. **Propagate**: If updating, optionally update directly related memories:
   - Max depth: 2
   - Max writes: 3
   - Max total touched: 5
6. **Defer**: If propagation budget exhausted, store as `~maintenance_pending`
7. **Return**: Compact outcome to parent

#### Rejection Reasons

Return these to parent when rejecting:

- `insufficient_specificity`: "Describes vague intention, not stable fact or concrete event"
- `ambiguous_target`: "Multiple memories match, cannot determine which to update"
- `unverified_conflict`: "Conflicts with stored memory, new input has insufficient evidence"
- `not_memory_worthy`: "Transient working context, should stay in session"
- `missing_structure`: "Lacks required fields for durable record"

#### Outcome States

Return one of these to parent:

- `captured`: New memory created
- `updated`: Existing memory revised
- `updated_with_propagation`: Updated plus related memories changed
- `deferred`: Some work queued for maintenance agent
- `skipped`: Valid but not stored (redundant/low-value)
- `rejected`: Cannot capture safely

## Available CLI Commands

### Store a Memory

```bash
file-memory store <key> '<json_or_markdown>' --format json|markdown --tags tag1,tag2
file-memory store <key> --file /path/to/content.json --format json
```

### Get a Memory

```bash
file-memory get <key>
file-memory get <key> --json
```

### List Memories

```bash
file-memory list-memories
file-memory list-memories --tag work
file-memory list-memories --json
```

### Search

```bash
file-memory search <query>
file-memory search <query> --json
```

### Update

```bash
file-memory update <key> '<new_content>'
file-memory update <key> --file /path/to/new_content.json
```

### Delete

```bash
file-memory delete <key>
```

### List Tags

```bash
file-memory list-tags
file-memory list-tags --json
```

## Memory Naming Conventions

- **Episodic**: `YYYY-MM-DD_event_description` or `session_event_description`
- **Semantic**: `preference_name`, `fact_topic`, `convention_tool`
- **System**: Prefixed with `~` (e.g., `~maintenance_pending`)

## Output Schema

When retrieving with `--json`:

```json
{
  "metadata": {
    "key": "my_key",
    "format": "json",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
    "tags": ["work", "important"],
    "memory_type": "semantic"
  },
  "content": {...}
}
```

## Reserved Prefixes

- `~`: System/internal memories (e.g., `~maintenance_pending`)

## Notes

- Memories persist until deleted
- Each memory is a separate file
- Schema version tracked for compatibility
- Key collisions detected and prevented
- Capture always searches before writing
- Propagation is bounded by budget
