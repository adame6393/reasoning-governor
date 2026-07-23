#!/usr/bin/env python3
"""Deterministically map described task stages to reasoning routes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TASK_CLASS_WEIGHT = {
    "mechanical": 0,
    "retrieval": 1,
    "synthesis": 2,
    "analytical": 3,
    "consequential": 4,
}

FACTOR_WEIGHTS = {
    "judgment": 2,
    "ambiguity": 1,
    "stakes": 2,
    "evidence_conflict": 1,
    "verification_difficulty": 1,
    "tool_depth": 1,
}

EFFORT_ORDER = ["none", "low", "medium", "high", "xhigh"]


def require_rating(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 3:
        raise ValueError(f"{field} must be an integer from 0 to 3")
    return value


def at_least(effort: str, floor: str) -> str:
    return EFFORT_ORDER[max(EFFORT_ORDER.index(effort), EFFORT_ORDER.index(floor))]


def route_stage(stage: dict[str, Any], allow_xhigh: bool) -> dict[str, Any]:
    stage_id = stage.get("id")
    if not isinstance(stage_id, str) or not stage_id.strip():
        raise ValueError("each stage must have a non-empty string id")

    task_class = stage.get("class")
    if task_class not in TASK_CLASS_WEIGHT:
        allowed = ", ".join(TASK_CLASS_WEIGHT)
        raise ValueError(f"{stage_id}.class must be one of: {allowed}")

    deterministic = stage.get("deterministic", False)
    if not isinstance(deterministic, bool):
        raise ValueError(f"{stage_id}.deterministic must be a boolean")

    factors = stage.get("factors", {})
    if not isinstance(factors, dict):
        raise ValueError(f"{stage_id}.factors must be an object")

    ratings = {
        name: require_rating(factors.get(name, 0), f"{stage_id}.factors.{name}")
        for name in FACTOR_WEIGHTS
    }

    if deterministic and ratings["judgment"] == 0 and ratings["ambiguity"] == 0:
        return {
            "id": stage_id,
            "route": "deterministic",
            "model_role": "none",
            "score": 0,
            "reasons": ["fully specified mechanical work should use code or tools"],
        }

    score = TASK_CLASS_WEIGHT[task_class] * 2 + sum(
        ratings[name] * weight for name, weight in FACTOR_WEIGHTS.items()
    )

    if score <= 4:
        effort = "none"
    elif score <= 9:
        effort = "low"
    elif score <= 16:
        effort = "medium"
    elif score <= 23:
        effort = "high"
    else:
        effort = "xhigh"

    reasons: list[str] = [f"weighted routing score {score}"]

    if ratings["tool_depth"] >= 2:
        effort = at_least(effort, "low")
        reasons.append("multi-step tool use requires at least low reasoning")
    if ratings["stakes"] >= 2:
        effort = at_least(effort, "medium")
        reasons.append("material consequences require at least medium reasoning")
    if ratings["stakes"] == 3 and ratings["judgment"] >= 2:
        effort = at_least(effort, "high")
        reasons.append("high-stakes judgment requires at least high reasoning")
    if effort == "xhigh" and not allow_xhigh:
        effort = "high"
        reasons.append("xhigh disabled; use high and escalate only after validation failure")

    model_role = {
        "none": "efficient",
        "low": "efficient",
        "medium": "capable",
        "high": "most-capable",
        "xhigh": "most-capable",
    }[effort]

    return {
        "id": stage_id,
        "route": effort,
        "model_role": model_role,
        "score": score,
        "reasons": reasons,
    }


def route_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict):
        raise ValueError("input must be a JSON object")
    stages = plan.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("stages must be a non-empty array")
    constraints = plan.get("constraints", {})
    if not isinstance(constraints, dict):
        raise ValueError("constraints must be an object")
    allow_xhigh = constraints.get("allow_xhigh", False)
    if not isinstance(allow_xhigh, bool):
        raise ValueError("constraints.allow_xhigh must be a boolean")

    routes = [route_stage(stage, allow_xhigh) for stage in stages]
    return {
        "routes": routes,
        "notes": [
            "Treat scores as routing aids, not proof of quality.",
            "Use the nearest supported effort level in the current environment.",
            "Escalate when evidence or validation triggers warrant it.",
        ],
    }


def self_test() -> None:
    plan = {
        "stages": [
            {
                "id": "normalize",
                "class": "mechanical",
                "deterministic": True,
                "factors": {},
            },
            {
                "id": "browse",
                "class": "retrieval",
                "factors": {"tool_depth": 2, "ambiguity": 1},
            },
            {
                "id": "forecast",
                "class": "consequential",
                "factors": {
                    "judgment": 3,
                    "ambiguity": 2,
                    "stakes": 3,
                    "evidence_conflict": 2,
                    "verification_difficulty": 3,
                    "tool_depth": 1,
                },
            },
        ],
        "constraints": {"allow_xhigh": False},
    }
    result = route_plan(plan)
    actual = [item["route"] for item in result["routes"]]
    expected = ["deterministic", "low", "high"]
    if actual != expected:
        raise AssertionError(f"expected {expected}, received {actual}")
    print("self-test passed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", nargs="?", help="JSON plan file; omit to read stdin")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    parser.add_argument("--self-test", action="store_true", help="run built-in tests")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        self_test()
        return 0

    try:
        raw = Path(args.plan).read_text(encoding="utf-8") if args.plan else sys.stdin.read()
        result = route_plan(json.loads(raw))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
