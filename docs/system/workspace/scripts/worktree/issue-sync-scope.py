#!/usr/bin/env python3
"""Scope merge-time issue sync to the lane's own raw issue.

pr-merge-guarded must only advance/close the issue that belongs to the branch
being merged.  A diff can legitimately touch other raw docs (platform parity
backfills, materialization); those are governance data, not this lane's
lifecycle and must never be closed by the merge.

Usage:
  python3 issue-sync-scope.py --raw-key <YYYYMMDDTHHMMSSZ> < issue-id-list
Reads one issue id per line from stdin, prints the kept ids.
"""
import argparse
import re
import sys


def filter_issue_ids(issue_ids, raw_key):
    """Keep ids that belong to raw_key (raw-<key> / I-<key>-*); no key = pass-through."""
    if not raw_key:
        return list(issue_ids)
    pattern = re.compile(re.escape(raw_key))
    return [issue_id for issue_id in issue_ids if pattern.search(issue_id)]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Filter issue ids to one lane raw key")
    parser.add_argument("--raw-key", default="", help="branch raw key; empty keeps all ids")
    args = parser.parse_args(argv)
    ids = [line.strip() for line in sys.stdin if line.strip()]
    for issue_id in filter_issue_ids(ids, args.raw_key):
        print(issue_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
