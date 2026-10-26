import unittest

from lead_caller.scoring import score_answers


class ScoringTests(unittest.TestCase):
    def test_hot_lead(self):
        s = score_answers({"budget": "set", "timeline": "now", "authority": "decision_maker"})
        self.assertEqual(s, {"score": 90, "tier": "hot"})

    def test_warm_lead(self):
        s = score_answers({"budget": "flexible", "timeline": "this_quarter", "authority": "influencer"})
        self.assertEqual(s, {"score": 50, "tier": "warm"})

    def test_cold_lead(self):
        s = score_answers({"budget": "none", "timeline": "exploring", "authority": "unknown"})
        self.assertEqual(s, {"score": 0, "tier": "cold"})

    def test_unknown_never_inflates(self):
        s = score_answers({"budget": "set"})
        self.assertEqual(s["score"], 35)
        self.assertEqual(s["tier"], "cold")


if __name__ == "__main__":
    unittest.main()
