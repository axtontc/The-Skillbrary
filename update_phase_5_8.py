import sys
import os
import uuid
import json
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".agents", "state")))
from lock_manager import append_to_ledger

def main():
    ledger_path = os.path.join(os.path.dirname(__file__), ".agents", "state", "ledger.jsonl")
    
    # Ensure file exists and is openable with r+
    if not os.path.exists(ledger_path):
        with open(ledger_path, 'w') as f:
            f.write("")
            
    payload = {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_id": "Phase_5_8_Retrospective_Analyst",
        "action": "RETROSPECTIVE_COMPLETE",
        "payload": {"status": "success"},
        "status": "COMMITTED"
    }
    
    append_to_ledger(ledger_path, json.dumps(payload))
    print("Appended Phase 5.8 completion to ledger.")

if __name__ == "__main__":
    main()
