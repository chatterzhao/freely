#!/usr/bin/env python3
"""Batch git object reader for governance gates.

Single truth for reading governance documents from the three views the merge
gate supports:

    staged view  ->  ``:path``            (git index)
    range view   ->  ``REF:path``         (source branch of a guarded merge)
    disk view    ->  ``ROOT_DIR/path``    (worktree filesystem)

Historically every ``staged_path_exists`` / ``range_path_exists`` /
``read_repo_text`` call spawned its own ``git cat-file -e`` or ``git show``
process.  ``build_issue_index()`` alone took 3423 subprocesses (~55s here).
This module keeps **one** long-lived ``git cat-file --batch`` process and an
in-process cache, so the whole gate needs a handful of processes.

Semantics are deliberately identical to the old implementation:

* ``read_repo_text`` still resolves staged > range > disk; this module does
  not decide priority.
* Blob bytes from ``cat-file --batch`` are byte-identical to ``git show``
  (verified for both ``:path`` and ``REF:path``).  Because the old code used
  ``subprocess.check_output(..., text=True)``, universal-newline conversion
  is applied here too, with the same strict UTF-8 decoding.
* A non-blob or unparsable response falls back to the original single-shot
  ``git show`` / ``git cat-file -e`` so no edge case silently changes.
"""

from __future__ import annotations

import subprocess
from typing import Dict, Optional


class _NonBlobResponse(Exception):
    """The batch response is not a plain blob; caller must use the fallback."""


class RepoView:
    def __init__(self, root: str):
        self.root = root
        self._proc: Optional[subprocess.Popen] = None
        self._cache: Dict[str, Optional[bytes]] = {}

    # ── batch transport ────────────────────────────────────────────────
    def _ensure_process(self) -> subprocess.Popen:
        if self._proc is None:
            self._proc = subprocess.Popen(
                ["git", "cat-file", "--batch"],
                cwd=self.root,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
        return self._proc

    def _query(self, spec: str) -> Optional[bytes]:
        """Return blob bytes for ``spec``, None when missing.

        Raises ``_NonBlobResponse`` when git answers with a tree/tag/commit or
        an unrecognised header — the caller then uses the legacy one-shot
        commands, preserving the original behaviour exactly.
        """
        if spec in self._cache:
            return self._cache[spec]
        proc = self._ensure_process()
        assert proc.stdin is not None and proc.stdout is not None
        try:
            proc.stdin.write((spec + "\n").encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline()
        except (BrokenPipeError, OSError):
            self._reset()
            raise _NonBlobResponse()
        if not header:
            self._reset()
            raise _NonBlobResponse()
        line = header.decode("utf-8", "replace").rstrip("\n")
        if line.endswith(" missing") or line.endswith(" ambiguous"):
            self._cache[spec] = None
            return None
        parts = line.split(" ")
        if len(parts) != 3 or parts[1] != "blob":
            # Consume any payload so the stream stays aligned, then let the
            # caller fall back instead of guessing at tree/tag semantics.
            self._reset()
            raise _NonBlobResponse()
        try:
            size = int(parts[2])
        except ValueError:
            self._reset()
            raise _NonBlobResponse()
        body = proc.stdout.read(size)
        proc.stdout.read(1)  # trailing newline after the payload
        self._cache[spec] = body
        return body

    def _reset(self) -> None:
        """Drop the batch process after a non-blob/unparsable response."""
        proc, self._proc = self._proc, None
        if proc is not None:
            try:
                if proc.stdin:
                    proc.stdin.close()
                proc.terminate()
                proc.wait(timeout=2)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

    def close(self) -> None:
        self._reset()

    # ── public contract ────────────────────────────────────────────────
    def peek(self, spec: str) -> Optional[bytes]:
        """Blob bytes for a staged/range spec, or None if missing.

        ``_NonBlobResponse`` is intentionally allowed to propagate: the merge
        gate falls back to the legacy one-shot command in that case.
        """
        return self._query(spec)

    def exists(self, spec: str) -> bool:
        try:
            return self._query(spec) is not None
        except _NonBlobResponse:
            return subprocess.run(
                ["git", "cat-file", "-e", spec],
                cwd=self.root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode == 0

    def read_text(self, spec: str) -> str:
        """Text of a staged/range spec, matching ``git show`` + text=True."""
        try:
            body = self._query(spec)
        except _NonBlobResponse:
            body = None
        if body is None:
            return subprocess.check_output(
                ["git", "show", spec], cwd=self.root, text=True
            )
        # subprocess text=True uses universal newlines + strict UTF-8.
        return body.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")

    def staged_path_exists(self, rel_path: Optional[str]) -> bool:
        if not rel_path:
            return False
        return self.exists(f":{rel_path}")

    def range_path_exists(self, rel_path: Optional[str], ref: str) -> bool:
        if not rel_path or not ref:
            return False
        return self.exists(f"{ref}:{rel_path}")
