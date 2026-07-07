import requests
import json

print("Searching Skillbrary for syntax checker...")
res = requests.get("http://localhost:8080/skills/search?intent=syntax")
skills = res.json()

if not skills:
    print("No skills found.")
    exit(1)

skill_id = skills[0]['id']
print(f"Found skill: {skill_id}. Executing via Sandbox...")

payload = {
    "intent": "syntax",
    "skill_id": skill_id
}
res = requests.post("http://localhost:8080/skills/execute", json=payload)

print("\n--- Execution Result ---")
if res.status_code == 200:
    print(res.json().get("output", "No output returned."))
else:
    print(f"Error {res.status_code}: {res.text}")
