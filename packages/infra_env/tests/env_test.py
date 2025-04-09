import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from infra_env import env


class TestLoadEnv(unittest.TestCase):
    def test_load_env_exact_level(self):
        with TemporaryDirectory() as tmp:
            parent = Path(tmp)
            child = parent / "subdir"
            child.mkdir()

            env_path = parent / ".env"
            env_path.write_text("FOO=bar")

            fake_file = child / "dummy.py"
            with patch.object(env, "__file__", str(fake_file)):
                loaded = env.load_env(level=1, recursive=False)
                self.assertTrue(loaded)
                self.assertEqual(os.getenv("FOO"), "bar")

    def test_load_env_recursive(self):
        with TemporaryDirectory() as tmp:
            parent = Path(tmp)
            child = parent / "subdir"
            child.mkdir()
            env_path = parent / ".env"
            env_path.write_text("BAR=baz")

            with patch.object(env, "__file__", str(child / "script.py")):
                loaded = env.load_env(level=2, recursive=True)
                self.assertTrue(loaded)
                self.assertEqual(os.getenv("BAR"), "baz")

    def test_load_env_not_found(self):
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            with patch.object(env, "__file__", str(base / "dummy.py")):
                loaded = env.load_env(level=1, recursive=False)
                self.assertFalse(loaded)


if __name__ == "__main__":
    unittest.main()
