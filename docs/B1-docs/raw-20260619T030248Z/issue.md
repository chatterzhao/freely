---
local_id: raw-20260619T030248Z48Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T030248Z-A
platform_ids:
  github:
    issue_id: '3009'
    url: https://github.com/chatterzhao/freely/issues/3009
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T03:03:07Z'
updated_at: '2026-06-19T03:13:47Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## 问题

`fix/raw-20260618T091116Z41Z-platform-sync` worktree 中 199 个 issue.md 被 `issue-sync` 改脏（git 未 add 的 modified）。

实际分析发现是三个独立问题，分别涉及不同的代码逻辑：

---

## 问题 1：`updated_at` 无脑刷新（168 个文件，85%）

只改了 1 行：`updated_at` 被刷成 sync 运行时间。这些老 issue 早已完成平台同步（已有 `platform_ids`），但 issue-sync 每次跑 batch 还是全部写一遍。

```
-updated_at: '2026-06-17T00:20:08Z'
+updated_at: '2026-06-18T12:22:54Z'
```

**根因**：issue-sync 的 `cmd_create()`、`cmd_update()`、`cmd_close()` 等无条件写 `updated_at`，没有判断"值是否真的变了"。`updated_at` 语义应是"内容最后变更时间"，但被当"最后同步时间"在用。

**涉及代码**：`bin/issue-sync` 多处 `_fm_set_str "$file" "updated_at" "$(date -u +...)"` 调用：
- `cmd_create()` 约 467 行
- `cmd_update()` 约 498 行
- `cmd_close()` 约 598-599 行

---

## 问题 2：YAML 引号风格不保留（约 23 个文件）

PyYAML `yaml.dump()` 重序列化整个 frontmatter 时，不保留原始引号选择：

| 字段 | 原始 | yaml.dump 后 | 方向 |
|------|------|-------------|------|
| `canonical_issue_path: ""` | `""` | `''` | 双→单 |
| `pre_tests_path: ""` | `""` | `''` | 双→单 |
| `absorbed_into: 'I-xxx'` | 有引号 | 无引号 | 单→无 |
| `created_at: 2026-06-17T00:00:00Z` | 无引号 | `2026-06-17 00:00:00+00:00` | 被解析为 datetime |

**根因**：`yaml.dump()` 使用自己的规则决定引号，完全不保留原始格式。当时序格式被 PyYAML 解析为 `datetime` 对象后再 dump，`T` 变空格、`Z` 变 `+00:00`。

**涉及代码**（4 处 `yaml.dump()`）：
1. `bin/issue-sync:65` — `_fm_set()`
2. `bin/issue-sync:370` — `_update_platform_ids()`
3. `bin/issue-sync:558` — `cmd_comment()`
4. `docs/system/workspace/scripts/sync/platform-adapter.py:401` — `pull_raw_issue()`

**修复方向**：用 `ruamel.yaml` RoundTripLoader/Dumper 替代 PyYAML，保留原始格式。

---

## 问题 3：`created_at` 数据错误（约 7 个文件）

最严重。部分新 I-* issue 的 frontmatter 缺失 `created_at`/`updated_at` 字段，issue-sync 把它们全部填成了 **sync 运行时间**，而非真实创建时间：

```yaml
# 原始文件中 created_at 不存在
# issue-sync 后：
created_at: '2026-06-18T12:16:21Z'   ← 这是 sync 时间，不是创建时间
```

**根因**：`_update_platform_ids()` 和 `cmd_create()` 中构建 frontmatter dict 时，如果原文件缺少 `created_at`，用 `datetime.now()` 填充，而非从文件 mtime 或原始 title 时间戳推断。

**涉及代码**：`bin/issue-sync` 的 `_update_platform_ids()` 约 357-374 行、`cmd_create()` 约 467 行。

---

## 总结

| 问题 | 文件数 | 严重程度 | 性质 |
|------|--------|----------|------|
| 1. `updated_at` 无脑刷新 | 168 | 高（噪声） | issue-sync 逻辑缺陷 |
| 2. YAML 引号格式丢失 | ~23 | 中 | yaml.dump 序列化器 |
| 3. `created_at` 数据损坏 | ~7 | **严重** | issue-sync 逻辑缺陷 |

问题 1 和 3 是 issue-sync 的逻辑问题，问题 2 是 PyYAML 的序列化问题。建议分开修复。
