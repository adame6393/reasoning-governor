# Routing examples

## Residential comparable-sales analysis

1. Plan location and property-specific searches: medium.
2. Browse and extract sale records: low, using an efficient model where available.
3. Normalize dates, prices, addresses, and square footage: deterministic.
4. Deduplicate and enforce hard eligibility rules: deterministic or low.
5. Judge similarity and exclude weak comparables: medium.
6. Adjust for time, condition, size, location, and features: high.
7. Calculate ranges and sensitivity tables: deterministic code directed by the analyst.
8. Verify citations, arithmetic, and outliers: low or medium; escalate if checks fail.
9. Report a range, assumptions, uncertainty drivers, and limitations. Do not present the result as a formal appraisal.

If the user requests automatic model selection and retrieval is substantial, delegate steps 2–4 to an efficient or capable research worker and pass its structured evidence to a most-capable analyst for steps 5–9. Keep the workflow in one agent when the evidence set is small.

## Product research and purchase decision

1. Gather current specifications and prices: low.
2. Normalize features and remove duplicates: deterministic.
3. Match products to user requirements: medium.
4. Use high reasoning only when tradeoffs are consequential, requirements conflict, or evidence is incomplete.

## Repository change

1. Locate files and references: low.
2. Understand cross-component behavior and plan changes: medium.
3. Implement scoped edits: low or medium depending on ambiguity.
4. Run formatting and tests: deterministic tools.
5. Escalate debugging to high only for complex failures, concurrency, security boundaries, or unclear invariants.

## Requests that should remain single-stage

- Reformat supplied text.
- Answer a stable factual question from provided context.
- Rename a symbol in one known file and run a focused check.
- Perform a calculation that deterministic code can verify.
