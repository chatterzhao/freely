---
local_id: raw-20260621T005656Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T005656Z-A
platform_ids:
  github:
    issue_id: '3181'
    url: https://github.com/chatterzhao/freely/issues/3181
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T00:57:13Z'
updated_at: '2026-06-21T00:57:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`governance-merge-gate` 的 `build_issue_index()` (L642-663) 使用 `ROOT_DIR` 扫描 `docs/issues/`：

```python
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))

def build_issue_index():
    issues_dir = os.path.join(ROOT_DIR, "docs", "issues")  # ← 始终指向 develop 根
    if os.path.isdir(issues_dir):
        for d in sorted(os.listdir(issues_dir)):            # ← 文件系统扫描
```

`ROOT_DIR` 基于 `__file__`（脚本路径），不随 CWD 变化。#3174 的 worktree context fix 做了 `cd "$_wt_path"`，但 gate 的 `ROOT_DIR` 不变 → `build_issue_index()` 始终扫描 develop 根的 `docs/issues/`，找不到 fix 分支新增的 I-* 文件。

结果：从 develop 根运行 `pr-review-guarded <fix-branch>` 时 IBM Completeness 仍会失败。

## 修复

当 `--range` 模式激活时（`USE_RANGE_VIEW=True`），`build_issue_index()` 改用 `git ls-tree` 从 source ref 发现文件：

```python
def build_issue_index():
    paths = []
    if USE_RANGE_VIEW and RANGE_SOURCE_REF:
        # Discover files from the range source ref (fix branch)
        try:
            output = git("ls-tree", "--name-only", "-r", f"{RANGE_SOURCE_REF}:docs/issues/")
            for line in output.splitlines():
                line = line.strip()
                if line and (line.startswith("docs/B1-docs/raw-") or line.startswith("docs/issues/I-")):
                    if line.endswith("/issue.md"):
                        paths.append(line)
        except Exception:
            pass
    # Fallback: filesystem scan at ROOT_DIR
    if not paths:
        ...existing code...
```

## 影响文件
- `docs/system/workspace/scripts/quality/governance-merge-gate` — `build_issue_index()`
