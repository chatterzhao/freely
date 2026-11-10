---
schema_version: '1'
local_id: raw-20261110T093145Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T093145Z-A
platform_ids:
  github:
    issue_id: '4269'
    url: https://github.com/chatterzhao/freely/issues/4269
    synced_at: ''
  gitee:
    issue_id: IKUDBF
    url: https://gitee.com/zhaoquan/freely/issues/IKUDBF
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-parity/raw-20261110T093145Z/issues/I-20261110T093145Z-A.md
last_synced_comment_at:
  github: '2026-11-10T09:48:16Z'
  gitee: '2026-11-10T09:48:16Z'
hash: ''
created_at: '2026-11-10T09:31:45Z'
updated_at: '2026-11-10T09:48:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T093145Z-A
source_candidate: ''
completed_at: '2026-11-10T09:48:15Z'
closeout_note: ''
severity: P1
---

# fix: raw 副本一致性把代码块注释误当标题（物化缺 # 标题行时 PR 被误挡）

workflow_kind: fix

## 背景

R23.13（#4264）的 `pr-create-guarded` Step 0b 报「raw replicas are inconsistent」：

```
[PR-CREATE] raw replicas are inconsistent; resolve explicitly, then retry.
```

日志里三份副本的 title 分别是：

- GitHub: `fix: 状态协议 allowed_keys 漏登记 21 个 heredoc 写入键（兼容读取会抛错）`
- Gitee: 同上
- **local: `-> statefileerror: unknown state key: 'last_manager_continuity_generated'`**

本地 title 被解析成了 issue body 里 python 代码块的一行注释。

## 根因（develop `34d80fe18` 实测）

`docs/system/workspace/scripts/lifecycle/raw-reconciliation-gate.py::_local_record`：

```python
match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
if match:
    title = match.group(1).strip()
    body = body[match.end():].lstrip()
```

两个问题叠加：

1. **`wt-create` / `raw-issue-pull` 物化 raw 时不保证写 `# 标题` 行**。本轮 `raw-20261110T084522Z` 物化出的 `docs/B1-docs/.../issue.md` frontmatter 之后直接是 `workflow_kind: fix`，没有 `# ...`；而上一轮 `raw-20261110T081029Z` 的物化文档有 `# fix: 状态文件迁移第二族起...`。同样由 `feedback` 创建、同样走 `wt-create --source platform`，结果不一致。
2. **`^#\s+` 不排除 fenced code block**。body 里的 ```python 代码块含 `# -> StateFileError: unknown state key: ...` 注释，被当成文档标题，随后 `body = body[match.end():]` 还把标题之前的正文全部丢弃。

结果：本地 record 的 title 与 body 双双错误，`canonical_projection` 与双平台副本不一致，门禁 fail-closed 地挡住 PR。本轮靠**手工在 B1 文档补回 `# 标题` 行**才通过，属于人工绕过而不是修复。

## 影响

- 任何 `feedback` 建单时 body 含以 `# ` 开头的代码注释（python / shell 注释极常见）且标题行未被物化的 raw，都会在 `pr-create-guarded` / `pr-merge-guarded` / `wt-close` 的一致性检查处被挡。
- 更隐蔽的情况：物化文档**有** `# 标题` 但正文里也有 `# ` 注释时，re.search 取第一个匹配（标题在前），暂时不出错；一旦标题行丢失就静默错判。
- 这是「副本一致性检查本身不可信」，比单个 PR 被挡更值得修。

## 修复方案

1. **`_local_record` 解析标题时跳过 fenced code block**：逐行扫描，用 ``` / ~~~ 开关状态，只把代码块外的第一个 `^#\s+` 当标题。
2. **显式校验而非静默兜底**：若物化文档没有任何代码块外的 `# 标题` 行，应给出明确诊断 `missing_local_title`（指向物化流程），而不是拿任意 `# ` 行凑数。
3. **修物化真源**：`platform-adapter.py::pull_raw_issue` 在 strict/legacy 两个分支写 `issue.md` 时，保证从平台 title（去掉 `[RAW-...] ` 前缀）生成 `# <title>` 行；本轮与上一轮的差异消失。
4. **AT**：用含 python 代码块注释的 body 构造 raw，验证 ①有标题行时三副本一致 ②无标题行时给出明确诊断而非误判 ③物化后本地文档必含标题行。

## 验收标准

- RED：develop 上用一个「无 `# 标题` 行 + body 含 `# -> StateFileError` 注释」的本地 raw 跑 `--require-local`，当前会把注释当 title 并报 `content_diverged`（错误诊断）。
- GREEN：同样输入报 `missing_local_title`（或三副本 allow），且不把代码块注释当标题。
- GREEN：`wt-create` 物化后 `issue.md` 必有代码块外的 `# 标题` 行，且与平台 title 归一化一致。
- GREEN：三副本一致性检查对「标题行存在/缺失/含代码块注释」三种夹具给出正确结论；`bin/test-all --ci` 全绿。

## 不做

- 不放宽副本一致性检查（不跳过 fail-closed）。
- 不改 `canonical_projection` 的其它维度（labels / comments / state）。
- 不手工批量回填历史 B1 文档（物化流程修好后按需 `raw-issue-pull` 重建）。

### comment-20261110T094816Z
- source: system
- event: promote_finalized
- children: ["I-20261110T093145Z-A"]

拆解为以下任务:
1. [I-20261110T093145Z-A](will-be-updated)
