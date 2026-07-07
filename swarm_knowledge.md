# Swarm Knowledge (Project Insights & Context)

## Fundamental Truths & Paradigms
- **AST Topography Mandate**: Parsing Python code dynamically is a security risk. Gating must be performed by constructing an AST map of `imports`, `syscalls`, and `external_io`. Tier 3/4 skills are strictly routed based on topological features rather than subjective LLM readings.
- **WAL-Driven Execution (Idempotency)**: All terminal execution states must be pushed into `skills_wal.jsonl` rather than directly altering state variables. The read-model is eventually consistent via background indexing. 
- **Bulk Resolvers & Latency**: `CapabilityRouter` implements bulk matching for tags. N+1 external queries are explicitly rejected to maintain the strict <50ms resolution latency SLA.
- **Garbage Collection by Design**: The single Write-Ahead Log records intermediate and failed states (e.g. from sandboxed subprocesses), but the indexer aggressively garbage collects, mapping only `APPROVED` final states to the readable local index `skills.index.json`.

## Dead Ends Encountered
- **Subjective Safety Reading**: Attempting to pass skill code through LLM filters was rejected; latency is too high and precision is poor. Subprocess isolation paired with AST evaluation is the proven solution.
- **Direct FS Mutations**: Allowing skills to write anywhere is unsafe. Direct IO operations by the Antigravity core are banned unless coordinated via a valid `msvcrt` FileLock (`.agents/state/lock_manager.py`).
- **Synchronous Disk Syncs in Append Loop**: Calling `os.fsync()` synchronously during WAL appends violated the < 10ms hardware constraint. Flushing buffers locally relies on OS-level commits while preventing locking bottlenecks.
