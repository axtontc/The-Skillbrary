# Antigravity Skill Intelligence Layer (Skillbrary)

## Purpose
Give Antigravity the ability to discover, evaluate, cache, refine, and safely use external agentic skills.
The goal is to expand Antigravity's capabilities without requiring the core model to know every possible procedure internally.
Antigravity should use external skill libraries as searchable procedural memory, while maintaining its own local learned skill cache for repeated use.

## Core Concept
Antigravity should not load thousands of skills into context.
It should run an autonomous loop:

1. **Goal Assessment**: Evaluate state vs desired goal.
2. **Capability Search**: Search local learned skills first -> then external skills.sh
3. **Plan & Refine**: Draft task-specific constraints and wrappers for the skill.
4. **Fauxton Review**: Check against `ollama-system-mapper` context to ensure architectural safety.
5. **Execution & Validation**: Run skill in sandbox and verify output.
6. **Record Failure/Success**: Cache skill on success, update success score. Log failure and loop back.

## Modules to Implement
1. **Skill Registry**: Local file structure (`.antigravity/skills/skills.index.json`, `skills.lock.json`, `learned-skills.md`) and CRUD operations to read/write manifests.
2. **Capability Router (skills.sh Bridge)**: Search and retrieval mechanism to query the external registry and translate into `SkillManifest` types.
3. **Fauxton Integration**: Wire up routing logic to halt and request approval from `fauxton` for Tier 3/4 skills.
4. **Skill Runtime (Sandbox Manager)**: The execution layer with strict file/network constraints.
5. **CLI Interface**: A simple entry point `src/main.py` that exposes the Capability Router to trigger a skill search and execution flow for a given user intent.

## Success Criteria
The Skill Intelligence Layer works when Antigravity can:
- discover useful skills
- avoid loading thousands of skills into context
- search local learned skills first
- retrieve external skills only when needed
- rank skills by trust, relevance, and prior success
- refine generic skills for specific tasks
- run external skills safely
- cache useful skills locally
- remember skill performance
- reuse known-good wrappers
- chain skills into workflows
- disable bad skills
- revalidate cached skills
- expand capability without bloating the core model
