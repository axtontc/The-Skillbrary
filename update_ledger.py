import os
import sys
import json
import uuid
import datetime

# Add the project root to sys.path so we can import lock_manager
project_root = r"C:\Users\axton\.gemini\antigravity\scratch\skillbrary"
sys.path.insert(0, project_root)

import importlib.util

lock_manager_path = os.path.join(project_root, ".agents", "state", "lock_manager.py")
spec = importlib.util.spec_from_file_location("lock_manager", lock_manager_path)
lock_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lock_manager)

ledger_path = os.path.join(project_root, ".agents", "state", "ledger.jsonl")

entry = {
    "transaction_id": str(uuid.uuid4()),
    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "agent_id": "Phase_4_9_Security_Auditor",
    "action": "SECURITY_AUDIT_COMPLETE",
    "payload": {"status": "clean"},
    "status": "COMMITTED"
}

with open(ledger_path, "a") as f:
    lock_manager.acquire_lock(f)
    try:
        f.write(json.dumps(entry) + "\n")
    finally:
        lock_manager.release_lock(f)
