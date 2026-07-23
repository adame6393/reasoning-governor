# Routing policy

Use this policy after decomposing the request into the smallest meaningful stages. Do not split a request solely to assign different labels.

## Stage factors

Rate each factor from 0 to 3:

| Factor | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Judgment | Mechanical | Light selection | Material synthesis | Novel or difficult judgment |
| Ambiguity | Fully specified | Minor gaps | Multiple plausible interpretations | Objective or constraints unclear |
| Stakes | Negligible | Reversible inconvenience | Material time or money | Safety, legal, financial, or irreversible impact |
| Evidence conflict | Consistent | Minor variation | Meaningful disagreement | Sparse or fundamentally conflicting |
| Verification difficulty | Exact check | Easy spot check | Requires multiple checks | No direct ground truth |
| Tool depth | No tools | One direct tool | Multi-step tools | Long-horizon or failure-prone tools |

Choose a task class: `mechanical`, `retrieval`, `synthesis`, `analytical`, or `consequential`.

Run the deterministic router:

```bash
python3 scripts/route_stages.py plan.json --pretty
```

The numerical score is a consistency aid, not ground truth. Apply the guardrails and quality floor after scoring.

## Default interpretation

| Route | Suitable work |
|---|---|
| Deterministic | Arithmetic, sorting, deduplication, transformations, schema and exact checks |
| None/minimal | Classification, formatting, or direct lookup with no meaningful ambiguity |
| Low | Retrieval, extraction, scanning, straightforward tool use, bounded drafting |
| Medium | Research synthesis, planning, comparison, data analysis, multi-step decisions |
| High | Difficult forecasting, complex debugging, consequential judgment, conflicting evidence |
| Xhigh or above | Exceptional long-horizon work where validation or evaluations demonstrate benefit |

## Model-role selection

- `efficient`: Prefer for low-reasoning scans, extraction, and supporting-document work.
- `capable`: Prefer for medium reasoning, synthesis, and most agentic work.
- `most-capable`: Prefer for high reasoning and consequential judgment.

Resolve these roles against models available in the current environment. Avoid hardcoding a model name in durable routing policy.

## Delegation gate

Delegate only if at least one condition holds:

- The stage is independent and can run concurrently.
- Its noisy intermediate context should be isolated from the final decision.
- A specialized tool or instruction set materially improves it.
- Independent verification is worth an additional model call.
- The user requested automatic model routing and a substantial stage maps to a materially different model role.

Keep work in the current agent when stages are short, tightly coupled, or require repeated context transfer.

When routing automatically, keep the root as the governor. Give each worker only its bounded input and request the stage handoff schema. Prefer sequential delegation when later work depends on earlier evidence; use parallel workers only for genuinely independent branches.

## Budget behavior

If the user provides a hard budget, reserve enough for final synthesis and verification before starting retrieval. Otherwise, use stage caps as guardrails rather than targets. Early-stop retrieval after evidence coverage is adequate, not after an arbitrary number of sources.
