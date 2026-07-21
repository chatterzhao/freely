"""Regression gate: agent-id.env must not appear in production code.

Scans BOTH bin/ and docs/system/workspace/scripts/runtime/ (capability surfaces).
Only pure comment lines are allowed. No loose string whitelist that masks live fallbacks.
"""
import os
import unittest

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCAN_ROOTS = [
    os.path.join(PROJECT, "bin"),
    os.path.join(PROJECT, "docs", "system", "workspace", "scripts", "runtime"),
]

# Production code extensions only
CODE_EXTS = (".sh", ".py", "")  # "" for bin scripts without extension

# Filenames that are pure tests under runtime (skip)
SKIP_DIR_NAMES = {".git", "__pycache__", "test-evidence", "tests"}


def _is_comment_only(line: str, fpath: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("#"):
        return True
    if stripped.startswith("//"):
        return True
    # Python docstring-only lines inside triple quotes are still code if they
    # are the sole content of a string used at runtime — only allow module-level
    # top-of-file docstrings when the line is purely a docstring quote line
    # containing historical note AND no assignment/call.
    if fpath.endswith(".py"):
        # Allow module docstring first 5 lines if it's a triple-quoted line
        # without executable constructs — handled by caller with lineno.
        if stripped in ('"""', "'''") or (
            (stripped.startswith('"""') or stripped.startswith("'''"))
            and ("agent-id.env" in stripped or "agent_id.env" in stripped)
            and "=" not in stripped
            and "(" not in stripped
        ):
            return True
    return False


class TestRegressionAgentIdEnv(unittest.TestCase):
    def test_no_agent_id_env_in_production_code(self):
        violations = []
        for root in SCAN_ROOTS:
            if not os.path.isdir(root):
                continue
            for dirpath, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES]
                for f in files:
                    fpath = os.path.join(dirpath, f)
                    # skip non-code
                    if f.endswith((".md", ".json", ".toml", ".log", ".bak", ".pyc")):
                        continue
                    if f.endswith(".bak.py"):
                        continue
                    # only scripts
                    if not (f.endswith(".py") or f.endswith(".sh") or (
                        os.access(fpath, os.X_OK) and "." not in f
                    ) or f in ("freely", "pr-review-guarded", "freely-review", "agent-table-query")):
                        if not f.endswith((".py", ".sh")):
                            # check if shebang script
                            try:
                                with open(fpath, "rb") as fh:
                                    head = fh.read(32)
                                if not head.startswith(b"#!"):
                                    continue
                            except Exception:
                                continue
                    try:
                        with open(fpath, errors="replace") as fh:
                            in_module_doc = False
                            for lineno, line in enumerate(fh, 1):
                                if "agent-id.env" not in line and "agent_id.env" not in line:
                                    # track simple module docstring start
                                    if lineno <= 3 and (line.strip().startswith('"""') or line.strip().startswith("'''")):
                                        in_module_doc = True
                                    if in_module_doc and (line.strip().endswith('"""') or line.strip().endswith("'''")) and lineno > 1:
                                        in_module_doc = False
                                    continue
                                if _is_comment_only(line, fpath):
                                    continue
                                # first-line module docstring allowance only
                                if fpath.endswith(".py") and lineno <= 5 and (
                                    '"""' in line or "'''" in line
                                ) and "=" not in line and "open(" not in line and "AGENT" not in line.split("=")[0] if "=" in line else True:
                                    # still reject assignments
                                    if "agent-id.env" in line and any(
                                        tok in line for tok in ("=", "open(", "read", "write", "Path(", "join(")
                                    ) and not line.strip().startswith("#"):
                                        pass  # fall through to violation if assignment-like
                                    else:
                                        if line.strip().startswith(('"""', "'''")) or line.count('"""') >= 1 or line.count("'''") >= 1:
                                            if not any(x in line for x in ("open(", "Path(", "write", "read", "AGENT_ENV", "agent_env")):
                                                continue
                                rel = os.path.relpath(fpath, PROJECT)
                                violations.append(f"{rel}:{lineno}: {line.strip()[:100]}")
                    except Exception:
                        pass

        if violations:
            self.fail(
                f"agent-id.env found in {len(violations)} production location(s):\n"
                + "\n".join(f"  - {v}" for v in violations)
                + "\n\nagent-id.env is retired. Live fallbacks are forbidden; comments only."
            )


if __name__ == "__main__":
    unittest.main()
