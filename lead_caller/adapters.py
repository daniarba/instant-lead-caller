"""Pluggable telephony and CRM adapters.

The flow talks to two seams: a TelephonyAdapter that dials and collects
answers, and a CRM webhook that receives the scored result. Mock adapters
let the whole pipeline run (and be tested) without a single provider account.
"""

import json
import urllib.request
from typing import Callable, Dict, List

from .models import CallResult, Lead


class TelephonyAdapter:
    """Place a call and walk the lead through the questions."""

    def place_call(self, lead: Lead, questions: List[str],
                   answer_factory: Callable[[str], str]) -> CallResult:
        raise NotImplementedError


class MockTelephony(TelephonyAdapter):
    """A scripted caller: answers come from a dict keyed by question index.

    Use it for demos, tests and load-shaping a real integration before
    you pay a provider for minutes.
    """

    def __init__(self, answers: Dict[str, str] = None, connect: bool = True):
        self.answers = answers or {}
        self.connect = connect

    def place_call(self, lead, questions, answer_factory):
        if not self.connect:
            return CallResult(connected=False)
        answers = {}
        for i, q in enumerate(questions):
            key = f"q{i}"
            answers[key] = self.answers.get(str(i), self.answers.get(q, "no answer"))
        return CallResult(connected=True, answers=answers)


class CRMWebhook:
    """POST the scored lead to a CRM/portal webhook endpoint."""

    def __init__(self, url: str, headers: Dict[str, str] = None):
        self.url = url
        self.headers = headers or {}

    def dispatch(self, payload: dict) -> int:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        headers.update(self.headers)
        req = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status
