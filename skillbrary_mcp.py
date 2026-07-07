import json
import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Skillbrary")

SKILLBRARY_URL = "http://localhost:8080"

@mcp.tool()
def search_skills(intent: str, limit: int = 10) -> str:
    """Search the external Skillbrary registries for agentic capabilities.
    
    Args:
        intent: The natural language intent or task description.
        limit: Max number of results to return.
    """
    try:
        res = requests.get(f"{SKILLBRARY_URL}/skills/search", params={"intent": intent, "limit": limit}, timeout=10.0)
        res.raise_for_status()
        return json.dumps(res.json(), indent=2)
    except Exception as e:
        return f"Error searching skills: {str(e)}"

@mcp.tool()
def install_skill(intent: str, skill_id: str) -> str:
    """Install a skill to the local agent toolbox so it is permanently available.
    
    Args:
        intent: The task intent.
        skill_id: The ID of the skill returned from search_skills.
    """
    try:
        payload = {"intent": intent, "skill_id": skill_id}
        res = requests.post(f"{SKILLBRARY_URL}/skills/install", json=payload, timeout=10.0)
        res.raise_for_status()
        return json.dumps(res.json(), indent=2)
    except Exception as e:
        return f"Error installing skill: {str(e)}"

@mcp.tool()
def execute_skill(intent: str, skill_id: str) -> str:
    """Execute a skill dynamically inside the SandboxManager.
    
    Args:
        intent: The task intent.
        skill_id: The ID of the skill returned from search_skills.
    """
    try:
        payload = {"intent": intent, "skill_id": skill_id}
        res = requests.post(f"{SKILLBRARY_URL}/skills/execute", json=payload, timeout=30.0)
        res.raise_for_status()
        return json.dumps(res.json(), indent=2)
    except Exception as e:
        return f"Error executing skill: {str(e)}"

import subprocess
import atexit
import time
import sys

if __name__ == "__main__":
    # Start the FastAPI server in a background subprocess
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api:app", "--host", "127.0.0.1", "--port", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Ensure the process is killed when MCP exits
    @atexit.register
    def cleanup():
        api_process.terminate()
        try:
            api_process.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            api_process.kill()

    # Give the API a moment to spin up by polling
    for _ in range(20):
        try:
            if requests.get(f"{SKILLBRARY_URL}/docs", timeout=1.0).status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)

    # Start the MCP server using stdio transport
    mcp.run()
