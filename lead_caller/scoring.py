"""Deterministic lead scoring. No LLM needed to say who is hot.

Rules, not vibes: budget tier, timeline urgency and decision authority
each carry points. Tests assert on these exact numbers.
"""

TIERS = {"hot": (75, 100), "warm": (45, 74), "cold": (0, 44)}

QUESTION_KEYS = ("budget", "timeline", "authority", "use_case")

BUDGET_POINTS = {"set": 35, "flexible": 20, "none": 0}
TIMELINE_POINTS = {"now": 35, "this_quarter": 20, "exploring": 0}
AUTHORITY_POINTS = {"decision_maker": 20, "influencer": 10, "unknown": 0}


def score_answers(answers: dict) -> dict:
    """Return {"score": 0..100, "tier": hot|warm|cold} from qualification answers.

    Unknown values score 0 rather than guessing, so a partial call never
    inflates a lead.
    """
    budget = answers.get("budget", "none")
    timeline = answers.get("timeline", "exploring")
    authority = answers.get("authority", "unknown")

    total = (BUDGET_POINTS.get(budget, 0)
             + TIMELINE_POINTS.get(timeline, 0)
             + AUTHORITY_POINTS.get(authority, 0))
    tier = next(t for t, (lo, hi) in TIERS.items() if lo <= total <= hi)
    return {"score": total, "tier": tier}
