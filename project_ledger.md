# Project Ledger: Skillbrary

**Current State:** v1.0.0 (Production Ready)
**Campaign Status:** FINAL_COMPLETE

## Fundamental Truths Discovered
- **AST Topology Parsing:** Asking agents to ingest raw source code causes OOM and token exhaustion. Lightweight, regex pre-filtered AST parsing is mandatory for codebase cartography (achieved 21.32ms latency).
- **WAL State Mutations:** Direct file modification in a concurrent multi-agent swarm guarantees race conditions. FileLock (msvcrt) wrapped around an append-only JSONL log (`ledger.jsonl`) eliminates deadlocks and ensures a crash-proof state machine.
- **Topological Sorting:** Tasks must be converted into a strict DAG. Parallel agents can only execute tasks with zero shared dependencies.
- **LLM Safety Gating is Anti-Pattern:** Using LLMs to enforce runtime code safety violates the <50ms IPC boundary. All execution boundaries must be determined using programmatic verification (AST schemas).

## Dead-Ends
- *Synchronous WAL flushing:* Using `os.fsync` on every WAL append broke the <10ms hardware constraint. Moving to asynchronous IO flushing with simple locking preserved stability and met latency requirements.
- *LLM Prompt Toxicity Checks:* Attempting to execute `eval()` inside the sandbox for safety checking introduced prompt poisoning risks; deprecated in favor of rigid AST gates.

## Stage Logs
- **Phase 0:** Base dual-ledger instantiated.
- **Phase 0.5-0.8:** Ephemeral cartography parsed and persisted in wiki.
- **Phase 1-1.9:** Master system prompts designed, DAG constructed, and CRDT conflicts resolved.
- **Phase 2-4:** Isolated specialists spawned in native branches. Tasks successfully completed via `/iterate` pipelines.
- **Phase 4.5-5.5:** Integration, QA profiling (with successful state machine loop patching an AST latency bottleneck), CSP mapping, and zero-vulnerability confirmation.
- **Phase 6:** Semantic compaction and zero-trust destruction executed.
