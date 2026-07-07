import ast
import time
import sys
import re

FAST_REJECT_REGEX = re.compile(
    r'\b(os|sys|subprocess|pty|socket|requests|urllib|http|ftplib|open)\b'
)

class ASTAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        self.syscalls = set()
        self.external_io = set()

        self.syscall_modules = {'os', 'sys', 'subprocess', 'pty'}
        self.io_modules = {'socket', 'requests', 'urllib', 'http', 'ftplib'}
        
        self.alias_map = {} # Maps alias to module or module.func

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
            self.alias_map[alias.asname or alias.name] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
            for alias in node.names:
                self.alias_map[alias.asname or alias.name] = f"{node.module}.{alias.name}"
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for open()
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name == 'open':
                self.external_io.add("builtin.open")
            elif func_name in self.alias_map:
                full_name = self.alias_map[func_name]
                mod = full_name.split('.')[0]
                if mod in self.syscall_modules:
                    self.syscalls.add(full_name)
                elif mod in self.io_modules:
                    self.external_io.add(full_name)
                
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                obj_name = node.func.value.id
                attr_name = node.func.attr
                
                if obj_name in self.alias_map:
                    mod = self.alias_map[obj_name]
                else:
                    mod = obj_name

                mod_base = mod.split('.')[0]
                if mod_base in self.syscall_modules:
                    self.syscalls.add(f"{mod}.{attr_name}")
                elif mod_base in self.io_modules:
                    self.external_io.add(f"{mod}.{attr_name}")

        self.generic_visit(node)

def analyze_source(source_code):
    start_time = time.perf_counter()

    if not FAST_REJECT_REGEX.search(source_code):
        end_time = time.perf_counter()
        return {
            "elapsed_ms": (end_time - start_time) * 1000,
            "imports": [],
            "syscalls": [],
            "external_io": []
        }

    tree = ast.parse(source_code)
    analyzer = ASTAnalyzer()
    analyzer.visit(tree)
    end_time = time.perf_counter()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    return {
        "elapsed_ms": elapsed_ms,
        "imports": sorted(list(analyzer.imports)),
        "syscalls": sorted(list(analyzer.syscalls)),
        "external_io": sorted(list(analyzer.external_io))
    }

if __name__ == "__main__":
    test_script = '''
import os
import requests
from subprocess import run as sp_run
import urllib.request as req

def do_stuff():
    f = open("test.txt", "w")
    f.write("hello")
    f.close()
    
    os.system("echo 'test'")
    sp_run(["ls", "-l"])
    
    r = requests.get("http://example.com")
    req.urlopen("http://example.com")
'''
    print("Running AST extraction...")
    result = analyze_source(test_script)
    print(f"Elapsed Time: {result['elapsed_ms']:.3f} ms")
    print(f"Imports: {result['imports']}")
    print(f"Syscalls: {result['syscalls']}")
    print(f"External IO: {result['external_io']}")

    if result['elapsed_ms'] < 100.0:
        print("PASS: Run time < 100ms")
        sys.exit(0)
    else:
        print("FAIL: Run time >= 100ms")
        sys.exit(1)
