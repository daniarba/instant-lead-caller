"""The qualification flow: dial fast, ask four questions, score, dispatch."""

import time
from typing import List

from .adapters import TelephonyAdapter
from .models import Lead
from .scoring import score_answers

DEFAULT_QUESTIONS = [
    "What project is this call about, in one line?",
    "Roughly what budget do you have in mind?",
    "When do you want this live?",
    "Are you the decision maker on this?",
]

# The answer key each question feeds, in the same order as DEFAULT_QUESTIONS.
ANSWER_KEYS = ("use_case", "budget", "timeline", "authority")


class QualificationFlow:
    def __init__(self, telephony: TelephonyAdapter,
                 questions: List[str] = None, max_delay_s: float = 30.0):
        self.telephony = telephony
        self.questions = questions or DEFAULT_QUESTIONS
        self.max_delay_s = max_delay_s

    def run(self, lead: Lead, submitted_at=None) -> dict:
        """Call the lead, score the answers, return the CRM payload.

        The whole point is speed: a form lead called within 30 seconds
        is still thinking about your service. The caller marks it stale
        past that window instead of pretending the lead is fresh.
        """
        stale = False
        if submitted_at is not None:
            try:
                age = time.time() - float(submitted_at)
                stale = age > self.max_delay_s
            except (TypeError, ValueError):
                stale = False

        result = self.telephony.place_call(lead, self.questions, answer_factory=None)
        if not result.connected:
            return {"lead": lead.as_dict(), "connected": False,
                    "outcome": "no_contact", "score": 0, "tier": "cold", "stale": stale}

        answers = {}
        for i, key in enumerate(ANSWER_KEYS):
            answers[key] = result.answers.get(f"q{i}", "no answer")
        scored = score_answers(answers)
        payload = {"lead": lead.as_dict(), "connected": True,
                   "answers": answers, "stale": stale, **scored}
        return payload
