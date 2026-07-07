import sys
import os
import uuid
import json
from datetime import datetime

# Adjust sys.path to be able to import lock_manager
sys.path.append(r"C:\Users\axton\.gemini\antigravity\scratch\skillbrary\.agents\state")

from lock_manager import append_to_ledger

ledger_path = r"C:\Users\axton\.gemini\antigravity\scratch\skillbrary\.agents\state\ledger.jsonl"

entry = {
    "transaction_id": str(uuid.uuid4()),
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "agent_id": "Phase_4_8_Sync_Checker",
    "action": "SYNC_CHECK_COMPLETE",
    "payload": {"status": "success"},
    "status": "COMMITTED"
}

append_to_ledger(ledger_path, json.dumps(entry))
