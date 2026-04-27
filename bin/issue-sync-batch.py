#!/usr/bin/env python3
"""issue-sync-batch: sync milestone issues to GitHub/Gitee.
Called by bin/issue-sync-bootstrap or run standalone.
Usage: python3 issue-sync-batch.py --repo chatterzhao/freely --batch 50 --issues-dir docs/issues
"""
import subprocess, os, re, sys, argparse
from datetime import datetime, timezone

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--batch', type=int, default=1)
    p.add_argument('--issues-dir', default='docs/issues')
    p.add_argument('--milestones', default='docs/milestones.md')
    p.add_argument('--dry-run', action='store_true')
    args = p.parse_args()

    # Collect issue IDs
    issue_ids = []
    if os.path.exists(args.milestones):
        with open(args.milestones) as f:
            content = f.read()
        pattern = r'`I-(\d{8}-\d{4}[A-Za-z0-9-]*)`'
        for m in sorted(set(re.findall(pattern, content))):
            issue_ids.append(f'I-{m}')

    # Skip already synced
    synced = set()
    if os.path.isdir(args.issues_dir):
        synced = set(d for d in os.listdir(args.issues_dir) if d.startswith('I-'))
    remaining = [i for i in issue_ids if i not in synced]

    batch = remaining[:args.batch]
    print(f"Total: {len(issue_ids)}, Synced: {len(synced)}, Remaining: {len(remaining)}, Batch: {len(batch)}")

    if args.dry_run:
        for i, lid in enumerate(batch[:20]):
            print(f"  [{i+1}] {lid}")
        if len(batch) > 20:
            print(f"  ... and {len(batch)-20} more")
        return

    synced_count = 0
    failed = []
    for local_id in batch:
        # Find canonical issue doc
        result = subprocess.run(
            ['find', 'docs/epics', '-path', '*/issues/*.md',
             '-exec', 'grep', '-l', local_id, '{}', ';'],
            capture_output=True, text=True
        )
        issue_file = result.stdout.strip().split('\n')[0] if result.stdout.strip() else ''

        if issue_file:
            with open(issue_file) as f:
                doc = f.read()
            title = doc.split('\n')[0].replace('# ', '')[:100]
            m = re.search(r'## (?:Why|Scope|Summary|Problem)\n(.*?)(?=\n## |\Z)', doc, re.DOTALL)
            summary = m.group(1).strip()[:500] if m else ''
            body = f"{summary}\n\ncanonical: {issue_file}"
        else:
            title = local_id
            body = f"Milestone issue: {local_id}"

        result = subprocess.run(
            ['gh', 'issue', 'create', '--repo', args.repo,
             '--title', title, '--body', body],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            url = result.stdout.strip()
            num = url.split('/')[-1]
            synced_count += 1

            os.makedirs(f'{args.issues_dir}/{local_id}', exist_ok=True)
            ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            with open(f'{args.issues_dir}/{local_id}/issue.md', 'w') as f:
                f.write(f"""---
local_id: {local_id}
kind: linked
status: completed
platform_ids:
  github:
    issue_id: "{num}"
    url: "{url}"
    synced_at: "{ts}"
primary_platform: github
canonical_issue_path: "{issue_file}"
last_synced_comment_at:
  github: "{ts}"
hash: ""
created_at: "{ts}"
updated_at: "{ts}"
---

{body[:2000]}
""")
            if synced_count % 10 == 0:
                print(f"  [{synced_count}/{len(batch)}] {local_id} -> {url}")
        else:
            failed.append(local_id)
            print(f"  [{synced_count}/{len(batch)}] {local_id}: FAILED - {result.stderr.strip()[:80]}")

    print(f"\nBatch: {synced_count} synced, {len(failed)} failed")
    if failed:
        print(f"Failed: {failed[:5]}")
    remaining_count = len(remaining) - synced_count
    if remaining_count > 0:
        print(f"Remaining: {remaining_count}")
        print(f"Next: python3 bin/issue-sync-batch.py --repo {args.repo} --batch {min(50, remaining_count)}")

if __name__ == '__main__':
    main()
