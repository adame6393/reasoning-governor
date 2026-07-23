# Reasoning Governor

A Codex skill that routes multi-stage AI work to the lowest-cost reasoning plan that preserves quality.

It decomposes mixed workflows by stage, selects an appropriate reasoning level and model role, prefers deterministic tools for exact work, and escalates only when evidence, stakes, or validation require it.

## Install

Install the skill from this repository with Codex's skill installer, using:

- Repository: `adame6393/reasoning-governor`
- Skill path: `reasoning-governor`

Or copy the `reasoning-governor` directory into your Codex skills directory.

## Use

Invoke it explicitly with `$reasoning-governor`, or ask Codex to optimize reasoning effort, model choice, verification, or token cost for a multi-stage task.

## Contents

- `SKILL.md`: core routing workflow and escalation rules
- `agents/openai.yaml`: UI metadata
- `references/`: routing policy, handoff schema, and examples
- `scripts/route_stages.py`: deterministic stage router

## License

MIT
