import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import audit_readonly  # noqa: E402


class AuditClassificationTests(unittest.TestCase):
    def test_envelope_success(self):
        kind, code, rows, detail = audit_readonly._describe({"code": 1, "message": "OK"})
        self.assertEqual(audit_readonly._classify("ok", kind, code, rows, detail), "pass")

    def test_non_empty_list_success(self):
        kind, code, rows, detail = audit_readonly._describe([{"rank": 1}])
        self.assertEqual(audit_readonly._classify("ok", kind, code, rows, detail), "pass")

    def test_empty_list_fails_required_check(self):
        kind, code, rows, detail = audit_readonly._describe([])
        self.assertEqual(audit_readonly._classify("ok", kind, code, rows, detail), "fail")

    def test_empty_list_passes_when_allowed(self):
        kind, code, rows, detail = audit_readonly._describe([])
        self.assertEqual(audit_readonly._classify("empty-ok", kind, code, rows, detail), "pass")

    def test_known_issue_is_not_a_failure(self):
        kind, code, rows, detail = audit_readonly._describe({"code": 6, "message": "AUTH FAILED"})
        self.assertEqual(audit_readonly._classify("known", kind, code, rows, detail), "known")

    def test_known_issue_that_starts_working_is_reported(self):
        kind, code, rows, detail = audit_readonly._describe({"code": 1, "message": "OK"})
        self.assertEqual(audit_readonly._classify("known", kind, code, rows, detail), "changed")


if __name__ == "__main__":
    unittest.main()
