"""Regression gate: agent-id.env must not appear in production code.

Per raw-20260720T120329Z acceptance criterion #8:
  "增加回归门禁：能力目录生产代码出现 agent-id.env 即失败"

This test fails if agent-id.env is read or written in any production script.
Comments and documentation references are excluded.
"""
import os, sys, unittest, subprocess

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT, "docs", "system", "workspace", "scripts")

# Allowed: documentation files that may reference agent-id.env historically
ALLOWED_PATTERNS = [
    "retired",            # "agent-id.env retired"
    "replaces",           # "replaces agent-id.env"
    "已废弃",             # Chinese: deprecated
    "退役",               # Chinese: retired
    "单真源",             # Chinese: single source of truth
    "治理",               # Chinese: governance
    "_legacy",            # legacy docs
    "B1-docs",            # B1 documentation (historical records)
    "B2-docs",            # B2 documentation (historical records)
    "three-loop",         # lifecycle documentation
    "SKILL.md",           # skill documentation
    "AGENTS.md",          # agent documentation
]

class TestRegressionAgentIdEnv(unittest.TestCase):
    """agent-id.env regression gate."""

    def test_no_agent_id_env_in_production_code(self):
        """agent-id.env must not be read/written in production scripts."""
        violations = []
        for root, dirs, files in os.walk(SCRIPTS_DIR):
            dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'test-evidence')]
            for f in files:
                if not f.endswith(('.sh', '.py')):
                    continue
                fpath = os.path.join(root, f)
                try:
                    with open(fpath) as fh:
                        for lineno, line in enumerate(fh, 1):
                            if 'agent-id.env' not in line and 'agent_id.env' not in line:
                                continue
                            rel = os.path.relpath(fpath, PROJECT)
                            # Check if line is a comment-only reference
                            stripped = line.strip()
                            if stripped.startswith('#') or stripped.startswith('//'):
                                continue
                            # Allow docstrings and error detail strings (not actual reads/writes)
                            if f.endswith('.py') and lineno <= 3:
                                continue  # module docstring
                            if 'detail' in line and 'agent_working' in line:
                                continue  # scan.py: detail message (not a file read)
                            if any(p in line for p in ALLOWED_PATTERNS):
                                continue
                            violations.append(f"{rel}:{lineno}: {stripped[:80]}")
                except Exception:
                    pass

        if violations:
            self.fail(
                f"agent-id.env found in {len(violations)} production code location(s):\n" +
                "\n".join(f"  - {v}" for v in violations) +
                "\n\nagent-id.env has been retired. All identity resolution must use agent_working table."
            )


if __name__ == "__main__":
    unittest.main()
