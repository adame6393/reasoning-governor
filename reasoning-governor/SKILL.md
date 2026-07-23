---
name: reasoning-governor
description: Route multi-stage AI work to appropriate reasoning effort, model capability, tools, and verification while controlling token cost. Use when a user asks to optimize AI tokens or cost, avoid manually switching models, apply different reasoning levels across research and analysis, choose the cheapest adequate model, create a reasoning budget, or complete a mixed workflow whose stages vary materially in complexity, uncertainty, or consequence.
---

# Reasoning Governor

Allocate reasoning by stage. Optimize for the lowest expected cost that still meets the user's quality requirement; never minimize tokens at the expense of a material accuracy or safety threshold.

## Core workflow

1. Define the outcome, quality floor, constraints, and consequence of error.
2. Decompose only when stages differ materially in cognitive work, tools, independence, or verification. Keep simple requests single-stage.
3. Route each stage using [references/routing-policy.md](references/routing-policy.md). For repeatability, pass stage factors to `scripts/route_stages.py`.
4. Execute deterministic operations with code or tools. Do not spend model reasoning on arithmetic, sorting, deduplication, schema validation, or exact comparisons when software can do them reliably.
5. Use the current agent for tightly coupled work. Delegate only bounded, independent, read-heavy stages when isolation, specialization, or parallelism is worth the extra request and context cost.
6. Pass compact structured results between stages using [references/handoff-schema.md](references/handoff-schema.md). Pass evidence and decisions, not raw browsing transcripts or hidden reasoning.
7. Run cheap objective checks first. Escalate only when an escalation trigger fires.
8. Deliver the requested result. Include a concise routing summary only when the user asked about cost, reasoning allocation, or transparency.

## Execution rules

- Treat task length and input size as weak signals. Route primarily on judgment, ambiguity, stakes, evidence conflict, verification difficulty, and tool depth.
- Separate model capability from reasoning effort. Prefer an efficient model for extraction and scanning, a capable model for synthesis, and the most-capable available model only for difficult consequential judgment.
- Use the closest supported reasoning level when a selected model lacks the routed level.
- Do not switch models merely to save a small number of tokens if the extra request, context replay, or coordination would cost more.
- Do not create a subagent for a trivial stage. Subagents perform their own model and tool work.
- When the user explicitly requests automatic model routing, use per-agent model and reasoning overrides for substantial stages whose expected savings or quality gain exceed handoff overhead. Keep the root agent as a lightweight governor and return only structured stage handoffs.
- If substantial retrieval feeds consequential analysis, prefer an efficient research worker and a separate most-capable analyst. Skip this split when retrieval is small enough that replaying context would cost as much as it saves.
- When per-agent model controls are unavailable, keep the current model and vary tool use, verification depth, and response scope. Do not imply that a model switch occurred.
- Do not expose private chain-of-thought. Report routing factors, evidence, checks, and conclusions.
- Do not claim savings without usage data. Describe expected efficiency or report measured tokens, latency, and cost when available.

## Escalation triggers

Escalate one level, re-plan, or request missing information when any of these materially affect the answer:

- Required evidence is missing, stale, contradictory, or low quality.
- The stage has high consequences and assumptions are not independently checkable.
- Small assumption changes cause a large outcome change.
- Deterministic checks fail.
- Independent analyses disagree beyond the task's tolerance.
- The current route cannot meet the stated quality floor.

Use `xhigh`, `max`, `ultra`, or a pro-style mode only when supported and when a hard task, failed validation, or measured evaluation benefit justifies the added cost and latency.

## Validation and completion

Before finishing:

- Verify citations and source-to-claim support for research tasks.
- Verify calculations with code where practical.
- Distinguish facts, assumptions, estimates, and unresolved uncertainties.
- Prefer ranges and sensitivity analysis over false precision for forecasts.
- For consequential forecasts or decisions, state the main uncertainty drivers and what new evidence could change the result.
- Stop when the quality floor is met; do not spend remaining budget merely because it exists.

Use [references/examples.md](references/examples.md) when a concrete routing pattern is helpful.
