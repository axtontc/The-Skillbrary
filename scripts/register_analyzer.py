from src.registry import SkillRegistry, SkillManifest

registry = SkillRegistry()

analyzer_skill = SkillManifest(
    id="python-static-analyzer",
    name="Python Static Analyzer",
    description="Checks Python code for attribute and variable issues using pylint.",
    version="1.0.0",
    source="local",
    tags=["python", "lint", "attribute", "variable", "static", "analyzer"],
    capabilities=["python_static_analysis"],
    inputs=["directory_path"],
    outputs=["analysis_report"],
    permissions=["read_file"],
    riskLevel="low",
    trustTier=1,
    installCommand='python -m pip install pylint --user && python -m pylint -E "C:/Users/axton/Documents/Scripts/For Fun/Nakhu"'
)

registry.register(analyzer_skill)
print("Analyzer skill registered.")
