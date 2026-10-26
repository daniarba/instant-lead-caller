import unittest

from lead_caller.adapters import MockTelephony
from lead_caller.flow import QualificationFlow
from lead_caller.models import Lead


class FlowTests(unittest.TestCase):
    def test_connected_call_scores(self):
        caller = MockTelephony(answers={"0": "salon", "1": "set", "2": "now", "3": "decision_maker"})
        flow = QualificationFlow(telephony=caller)
        out = flow.run(Lead(name="A", phone="+1000"))
        self.assertTrue(out["connected"])
        self.assertEqual(out["tier"], "hot")
        self.assertEqual(out["answers"]["budget"], "set")

    def test_no_contact_is_cold(self):
        flow = QualificationFlow(telephony=MockTelephony(connect=False))
        out = flow.run(Lead(name="A", phone="+1000"))
        self.assertFalse(out["connected"])
        self.assertEqual(out["outcome"], "no_contact")
        self.assertEqual(out["tier"], "cold")

    def test_stale_lead_is_marked(self):
        flow = QualificationFlow(telephony=MockTelephony(), max_delay_s=30.0)
        out = flow.run(Lead(name="A", phone="+1000"), submitted_at=1.0)
        self.assertTrue(out["stale"])

    def test_fresh_lead_not_stale(self):
        import time
        flow = QualificationFlow(telephony=MockTelephony(), max_delay_s=30.0)
        out = flow.run(Lead(name="A", phone="+1000"), submitted_at=time.time())
        self.assertFalse(out["stale"])


if __name__ == "__main__":
    unittest.main()
