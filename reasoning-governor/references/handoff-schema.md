# Stage handoff schema

Use a compact handoff when one stage feeds another. Omit empty optional fields.

```json
{
  "stage_id": "comparable-research",
  "status": "complete",
  "result": {},
  "evidence": [
    {
      "claim": "A relevant fact or extracted record",
      "source": "URL, file, or record identifier",
      "observed_at": "ISO-8601 timestamp when freshness matters",
      "confidence": "high"
    }
  ],
  "assumptions": [],
  "excluded_items": [
    {"item": "identifier", "reason": "why it was excluded"}
  ],
  "checks": [
    {"name": "deduplication", "status": "passed", "details": ""}
  ],
  "uncertainties": [],
  "escalation": {
    "needed": false,
    "reason": ""
  }
}
```

Rules:

- Preserve provenance for every material factual input.
- Separate observations from assumptions and derived estimates.
- Return normalized records rather than prose when downstream analysis is tabular.
- Summarize tool failures and missing coverage; do not paste full logs unless needed to diagnose.
- Never include private chain-of-thought. Include concise decision rationales and check results.
