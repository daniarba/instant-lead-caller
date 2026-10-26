"""CLI demo: python -m lead_caller --demo  (mock caller, no provider account)."""

import argparse
import json
import sys

from .adapters import MockTelephony, CRMWebhook
from .flow import QualificationFlow
from .models import Lead


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="instant-lead-caller")
    ap.add_argument("--demo", action="store_true", help="run the mock end-to-end demo")
    ap.add_argument("--name", default="Test Lead")
    ap.add_argument("--phone", default="+10000000000")
    ap.add_argument("--webhook", help="POST the scored result to this CRM webhook URL")
    args = ap.parse_args(argv)

    if not args.demo:
        ap.error("pass --demo (real telephony adapters are on the roadmap)")

    lead = Lead(name=args.name, phone=args.phone)
    caller = MockTelephony(answers={
        "0": "Booking more salon appointments without paying for a full-time receptionist",
        "1": "set",
        "2": "now",
        "3": "decision_maker",
    })
    flow = QualificationFlow(telephony=caller)
    payload = flow.run(lead)

    print(json.dumps(payload, indent=2))

    if args.webhook:
        status = CRMWebhook(args.webhook).dispatch(payload)
        print(f"webhook status: {status}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
