import os
import json
import subprocess
import re

REPOS = [
    "https://github.com/VoltAgent/awesome-agent-skills.git",
    "https://github.com/vercel-labs/skills.git",
    "https://github.com/softaworks/agent-toolkit.git",
    "https://github.com/VoltAgent/awesome-openclaw-skills.git"
]
EXTERNAL_REGISTRIES_DIR = os.path.expanduser("~/.antigravity/external_registries")

print("Syncing external registries...")
os.makedirs(EXTERNAL_REGISTRIES_DIR, exist_ok=True)
for repo_url in REPOS:
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(EXTERNAL_REGISTRIES_DIR, repo_name)
    if not os.path.exists(repo_path):
        subprocess.run(["git", "clone", repo_url, repo_path], capture_output=True)
    else:
        subprocess.run(["git", "-C", repo_path, "pull"], capture_output=True)

print("Building index...")
cache_file = os.path.expanduser("~/.gemini/antigravity/scratch/openclaw_index.txt")
count = 0
with open(cache_file, "w", encoding="utf-8") as out:
    out.write("=== OPENCLAW SKILLBRARY INDEX ===\n")
    for root, _, files in os.walk(EXTERNAL_REGISTRIES_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file == "manifest.json" or file.endswith(".json"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        skill_id = data.get("id", data.get("name", "unknown"))
                        desc = data.get("description", "No description")
                        out.write(f"- {skill_id}: {desc}\n")
                        count += 1
                except Exception:
                    pass
            elif file.endswith(".md"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            match = re.match(r'^\s*-\s*\[(.*?)\]\((.*?)\)\s*-\s*(.*)$', line)
                            if match:
                                s_id = match.group(1).strip()
                                desc = match.group(3).strip()
                                out.write(f"- {s_id}: {desc}\n")
                                count += 1
                except Exception:
                    pass

print(f"Successfully cached {count} skills to {cache_file}")
