from src.registry import SkillRegistry, SkillManifest

registry = SkillRegistry()

lint_skill = SkillManifest(
    id="local-python-linter",
    name="Python Syntax & Variable Checker",
    description="Lints Python files for syntax errors using py_compile and checks variables.",
    version="1.0.0",
    source="local",
    tags=["python", "lint", "syntax", "check", "errors"],
    capabilities=["python_syntax_check"],
    inputs=["directory_path"],
    outputs=["lint_report"],
    permissions=["read_file"],
    riskLevel="low",
    trustTier=1,
    installCommand="python -m compileall 'C:/Users/axton/Documents/Scripts/For Fun/Nakhu'"
)

registry.register(lint_skill)
print("Local skill registered.")
