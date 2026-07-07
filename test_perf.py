import time
import os
import sys

# Add the project root to sys.path so 'src' can be resolved
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.registry.wal_manager import WALManager
from src.router.capability_router import CapabilityRouter
from src.evaluator.ast_gate import generate_topology

def test_wal():
    # FileLock acquisition and append must complete in < 10ms.
    manager = WALManager(wal_path="skills_wal.jsonl", index_path="skills.index.json")
    payload = {"event": "test", "id": "test_id", "state": "APPROVED"}
    t0 = time.perf_counter()
    manager.append_mutation(payload)
    t1 = time.perf_counter()
    elapsed = (t1-t0)*1000
    assert elapsed < 10.0, f"WAL time {elapsed:.2f}ms exceeds 10ms limit"

def test_router():
    # Router mapping complete in < 50ms.
    router = CapabilityRouter(index_path="skills.index.json")
    t0 = time.perf_counter()
    _ = router.resolve_capabilities(["test"])
    t1 = time.perf_counter()
    elapsed = (t1-t0)*1000
    assert elapsed < 50.0, f"Router time {elapsed:.2f}ms exceeds 50ms limit"

def test_ast():
    # AST parsing for a < 1MB script in < 100ms.
    # 41000 * 21 bytes = 861 KB
    code = "def foo():\n    x = 1\n" * 41000
    t0 = time.perf_counter()
    res = generate_topology(code)
    t1 = time.perf_counter()
    elapsed = (t1-t0)*1000
    assert elapsed < 100.0, f"AST time {elapsed:.2f}ms exceeds 100ms limit"

if __name__ == "__main__":
    test_wal()
    test_router()
    test_ast()
