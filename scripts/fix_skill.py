from src.registry import SkillRegistry

registry = SkillRegistry()
skill = registry.get("local-python-linter")
if skill:
    skill.installCommand = 'python -m compileall "C:/Users/axton/Documents/Scripts/For Fun/Nakhu"'
    registry.register(skill)
    print("Fixed skill command.")
