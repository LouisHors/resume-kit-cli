import json
import unittest

from resume_kit.jsonio import error_envelope, success_envelope


class JsonEnvelopeTests(unittest.TestCase):
    def test_success_envelope(self):
        payload = success_envelope({"value": 1})
        self.assertEqual(payload["ok"], True)
        self.assertEqual(payload["data"]["value"], 1)
        self.assertEqual(payload["warnings"], [])

    def test_error_envelope_has_code_message_and_detail(self):
        payload = error_envelope("missing_source", "Missing source", {"path": "x"})
        self.assertEqual(payload["ok"], False)
        self.assertEqual(payload["error"]["code"], "missing_source")
        self.assertEqual(payload["error"]["message"], "Missing source")
        self.assertEqual(payload["error"]["detail"]["path"], "x")
        json.dumps(payload, ensure_ascii=False)
