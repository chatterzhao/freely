#!/usr/bin/env python3
"""RED/GREEN contract for declarative worktree seeds.

`git worktree add` only checks out tracked files.  Anything gitignored but
required to run (agent table, local env, certificates) has to be brought in
deliberately, and the list of such paths belongs to the project, not to a
hardcoded `cp` line inside wt-create.
"""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODULE = ROOT / "docs/system/workspace/scripts/worktree/worktree_seed.py"


def load():
    spec = importlib.util.spec_from_file_location("worktree_seed", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SeedManifestTests(unittest.TestCase):
    def setUp(self):
        self.subject = load()
        self.dir = tempfile.TemporaryDirectory()
        self.project = Path(self.dir.name) / "project"
        self.target = Path(self.dir.name) / "wt"
        (self.project / ".freely").mkdir(parents=True)
        (self.project / ".freely" / "agent-table.toml").write_text("version = 1\n")
        self.target.mkdir()

    def tearDown(self):
        self.dir.cleanup()

    def _manifest(self, body: str):
        path = self.project / "docs" / "system" / "workspace" / "worktree-seed.toml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        return path

    def test_builtin_default_seeds_the_agent_table(self):
        entries, source = self.subject.load(self.project)
        self.assertEqual(source, "builtin")
        report = self.subject.apply(self.project, self.target, entries)
        self.assertEqual(report["copied"], [".freely/agent-table.toml"])
        self.assertTrue((self.target / ".freely" / "agent-table.toml").is_file())

    def test_manifest_replaces_the_builtin_list(self):
        self._manifest('''
version = 1

[[seed]]
path = ".env"
required = true
''')
        entries, source = self.subject.load(self.project)
        self.assertEqual(source, "manifest")
        self.assertEqual([item["path"] for item in entries], [".env"])
        self.assertFalse(any(item["path"].endswith("agent-table.toml") for item in entries))

    def test_existing_target_is_never_overwritten(self):
        target_file = self.target / ".freely" / "agent-table.toml"
        target_file.parent.mkdir(parents=True)
        target_file.write_text("local edit\n")
        entries, _ = self.subject.load(self.project)
        report = self.subject.apply(self.project, self.target, entries)
        self.assertEqual(report["skipped"], [".freely/agent-table.toml"])
        self.assertEqual(target_file.read_text(), "local edit\n")

    def test_missing_required_source_fails_with_the_path(self):
        self._manifest('''
version = 1

[[seed]]
path = ".env"
required = true
''')
        entries, _ = self.subject.load(self.project)
        with self.assertRaises(self.subject.SeedError) as caught:
            self.subject.apply(self.project, self.target, entries)
        self.assertIn(".env", str(caught.exception))

    def test_missing_optional_source_is_reported_not_fatal(self):
        self._manifest('''
version = 1

[[seed]]
path = ".env"
required = false
''')
        entries, _ = self.subject.load(self.project)
        report = self.subject.apply(self.project, self.target, entries)
        self.assertEqual(report["missing"], [".env"])

    def test_paths_outside_the_project_are_rejected(self):
        self._manifest('''
version = 1

[[seed]]
path = "../secrets.env"
''')
        entries, _ = self.subject.load(self.project)
        with self.assertRaises(self.subject.SeedError):
            self.subject.apply(self.project, self.target, entries)

    def test_absolute_paths_are_rejected(self):
        self._manifest('''
version = 1

[[seed]]
path = "/etc/passwd"
''')
        entries, _ = self.subject.load(self.project)
        with self.assertRaises(self.subject.SeedError):
            self.subject.apply(self.project, self.target, entries)

    def test_link_mode_tracks_the_source_file(self):
        self._manifest('''
version = 1

[[seed]]
path = ".freely/agent-table.toml"
mode = "link"
''')
        entries, _ = self.subject.load(self.project)
        report = self.subject.apply(self.project, self.target, entries)
        self.assertEqual(report["linked"], [".freely/agent-table.toml"])
        seeded = self.target / ".freely" / "agent-table.toml"
        self.assertTrue(seeded.is_symlink())
        (self.project / ".freely" / "agent-table.toml").write_text("version = 2\n")
        self.assertEqual(seeded.read_text(), "version = 2\n")

    def test_directory_seed_copies_recursively(self):
        (self.project / "certs").mkdir()
        (self.project / "certs" / "a.pem").write_text("a")
        self._manifest('''
version = 1

[[seed]]
path = "certs"
''')
        entries, _ = self.subject.load(self.project)
        report = self.subject.apply(self.project, self.target, entries)
        self.assertEqual(report["copied"], ["certs"])
        self.assertTrue((self.target / "certs" / "a.pem").is_file())


if __name__ == "__main__":
    unittest.main()
