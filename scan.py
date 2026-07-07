import os
import re
import json

TARGET_DIR = r"C:\Users\axton\.gemini\antigravity\scratch\skillbrary"

PATTERNS = {
    "Secrets": r"(?i)(api_key|apikey|secret|password|token)\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]",
    "Dangerous Calls (eval/exec)": r"\b(eval|exec)\s*\(",
    "Dangerous Calls (os.system/subprocess)": r"\b(os\.system|subprocess\.Popen|subprocess\.call|subprocess\.run)\b",
    "Shell=True": r"shell\s*=\s*True",
    "Hardcoded IP/URLs": r"http://[0-9a-zA-Z\.]+|https://[0-9a-zA-Z\.]+"
}

def scan():
    results = []
    for root, dirs, files in os.walk(TARGET_DIR):
        if '.git' in root or '__pycache__' in root or '.agents' in root:
            continue
        for file in files:
            if not file.endswith('.py') and not file.endswith('.md') and not file.endswith('.json'):
                continue
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.readlines()
                    for i, line in enumerate(content):
                        for category, pattern in PATTERNS.items():
                            if re.search(pattern, line):
                                results.append({
                                    "file": filepath,
                                    "line_num": i + 1,
                                    "category": category,
                                    "match": line.strip()
                                })
            except Exception as e:
                pass
    
    with open(os.path.join(TARGET_DIR, "scan_results.json"), "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    scan()
