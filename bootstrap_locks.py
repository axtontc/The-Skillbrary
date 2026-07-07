import os
import json
import sys

# add current dir to sys.path to import src.evaluator.ast_gate
sys.path.insert(0, os.path.abspath("."))
from src.evaluator.ast_gate import generate_topology

locks = {}
src_dir = "src"

for root, dirs, files in os.walk(src_dir):
    if "__pycache__" in root: continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, src_dir)
            with open(path, "r", encoding="utf-8") as f:
                source = f.read()
            topology = generate_topology(source)
            locks[rel_path] = {
                "elapsed_ms": topology["elapsed_ms"],
                "imports": topology["imports"],
                "syscalls": topology["syscalls"],
                "external_io": topology["external_io"]
            }

with open("schema_locks.json", "w", encoding="utf-8") as f:
    json.dump(locks, f, indent=2)

print("Bootstrapped schema_locks.json")
