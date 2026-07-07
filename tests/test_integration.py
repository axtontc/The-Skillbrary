import os
import sys
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.registry.wal_manager import WALManager
from src.router.capability_router import CapabilityRouter
from src.evaluator.ast_gate import generate_topology
from src.runtime.sandbox import SkillSandbox

def test_wal_manager_atomic_append(tmp_path):
    wal_file = tmp_path / "skills_wal.jsonl"
    index_file = tmp_path / "skills.index.json"
    
    manager = WALManager(wal_path=str(wal_file), index_path=str(index_file))
    
    # Append an APPROVED skill
    manager.append_mutation({
        "event": "CREATE_SKILL",
        "id": "skill_alpha",
        "state": "APPROVED",
        "description": "Alpha skill"
    })
    
    manager.commit_index()
    
    # Check WAL
    with open(wal_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        assert len(lines) == 1
        payload = json.loads(lines[0])
        assert payload["id"] == "skill_alpha"
        assert payload["state"] == "APPROVED"
        
    # Check Index
    with open(index_file, "r") as f:
        index_data = json.load(f)
        assert "skill_alpha" in index_data
        assert index_data["skill_alpha"]["state"] == "APPROVED"
        
    # Append a PENDING skill
    manager.append_mutation({
        "event": "CREATE_SKILL",
        "id": "skill_beta",
        "state": "PENDING"
    })
    
    manager.commit_index()
    
    with open(index_file, "r") as f:
        index_data = json.load(f)
        assert "skill_beta" not in index_data

def test_capability_router(tmp_path):
    index_file = tmp_path / "skills.index.json"
    
    # Create fake index
    data = {
        "skill_a": {"id": "skill_a", "description": "skill_a", "state": "APPROVED"},
        "skill_b": {"id": "skill_b", "description": "skill_b", "state": "APPROVED"}
    }
    with open(index_file, "w") as f:
        json.dump(data, f)
        
    router = CapabilityRouter(index_path=str(index_file))
    skills = router.resolve_capabilities(["skill_a", "skill_c"])
    
    # Should return skill_a from local and ext_skill_c from external
    assert len(skills) == 2
    assert skills[0].id == "skill_a"
    assert skills[1].id == "ext_skill_c"

def test_ast_evaluator():
    code = "import os\ndef test():\n    x = 1\n    return x\n"
    topology = generate_topology(code)
    
    assert "imports" in topology
    assert "os" in topology["imports"]
    
def test_sandbox_runtime(tmp_path):
    script = tmp_path / "test_script.py"
    script.write_text("print('hello sandbox')")
    
    # Create fake WAL/Index
    wal_file = tmp_path / "skills_wal.jsonl"
    index_file = tmp_path / "skills.index.json"
    manager = WALManager(wal_path=str(wal_file), index_path=str(index_file))
    
    sandbox = SkillSandbox(wal_manager=manager)
    result = sandbox.execute_skill(skill_id="test_skill", script_path=str(script))
    
    assert result["sandbox_exec"]["return_code"] == 0
    assert "hello sandbox" in result["sandbox_exec"]["stdout"]
    assert result["state"] == "APPROVED"
