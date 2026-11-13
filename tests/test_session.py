import json
import os
import tempfile
import unittest
from pathlib import Path

from blockmango.config import Config
from blockmango.session import SessionStore


class SessionStoreTests(unittest.TestCase):
    def test_saved_sessions_are_private_and_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sessions.json"
            store = SessionStore(Config(session_cache_path=str(path)))
            session = {"uid": 12, "token": "test-token"}
            store.save("test-user", session)

            self.assertEqual(store.load("test-user"), session)
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(path.read_text()), {"test-user": session})


if __name__ == "__main__":
    unittest.main()
