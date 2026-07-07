import time
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.evaluator.ast_gate import generate_topology

# let's write 1MB of realistic looking code
code = "def foo():\n    x = 1\n    y = 2\n    z = x + y\n    return z\n" * 15000
print(f"Code size: {len(code.encode('utf-8')) / 1024:.2f} KB")
t0 = time.perf_counter()
res = generate_topology(code)
t1 = time.perf_counter()
print(f"AST elapsed inside parser: {res['elapsed_ms']:.2f} ms")
print(f"AST time total: {(t1-t0)*1000:.2f} ms")
