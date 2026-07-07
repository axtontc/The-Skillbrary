---
name: skillbrary
description: Queries the local Skill Intelligence Layer API (Skillbrary) on port 8080 to find and execute external agentic skills.
---

# Skillbrary Integration

The Skill Intelligence Layer (Skillbrary) runs locally as a FastAPI server on port 8080. It allows Antigravity to dynamically fetch, install, and execute over 6,000 capabilities from external repositories (such as the OpenClaw database).

## Usage

Whenever you encounter a task that requires a capability you do not currently possess, use this skill to search the external registries and either install or execute the required capability.

### 0. Search Guidelines (CRITICAL)

The Skillbrary uses a Tokenized AND Search. It checks if **all** keywords you provide exist anywhere in a skill's name, description, tags, or capabilities.
- **Rule 1**: Do NOT use full conversational sentences (e.g., `"find me a skill for UI layout"`).
- **Rule 2**: Extract 1-3 distinct keywords representing the core capability (e.g., `"ui layout"` or `"database"`).

### 1. Search for a Skill

Use Python to query the search endpoint. By default, it parses both `manifest.json` files and Markdown awesome-lists. You can optionally use the `limit` parameter.

```python
import requests
import json

intent = "your task intent"
res = requests.get(f"http://localhost:8080/skills/search?intent={intent}&limit=10")
skills = res.json()
print(json.dumps(skills, indent=2))
```

### 2. Execute the Skill

Once you identify the `skill_id` from the search results, trigger the execution endpoint. The execution will automatically run in the SandboxManager and go through Fauxton's approval cycle.

```python
import requests
import json

payload = {
    "intent": "your task intent",
    "skill_id": "the_skill_id"
}
res = requests.post("http://localhost:8080/skills/execute", json=payload)
print(json.dumps(res.json(), indent=2))
```

### 3. Install a Skill (Without Executing)

If you just want to add the skill to your native toolbox (e.g., generating a `SKILL.md` file in your `~/.gemini/config/skills/` directory) without immediately executing it in the sandbox, use the install endpoint:

```python
import requests
import json

payload = {
    "intent": "your task intent",
    "skill_id": "the_skill_id"
}
res = requests.post("http://localhost:8080/skills/install", json=payload)
print(json.dumps(res.json(), indent=2))
```

### Notes
- Ensure the server `python -m uvicorn src.api:app --host 0.0.0.0 --port 8080` is running in the background before querying.
- The router natively parses standard `manifest.json` files as well as Markdown awesome-list formats (`- [skill_id](url) - desc`).
