---
local_id: raw-20260507T0730Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
platform_ids:
  github:
    issue_id: '244'
    url: https://github.com/chatterzhao/freely/issues/244
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-07T10:46:27Z'
updated_at: '2026-06-29T13:42:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/epics/source-param/verification/pre-tests.md
verification_artifact_dir: docs/epics/source-param/code-reviews
source_candidate: docs/B1-docs/20260507-source-param/candidates.md
platform_state: closed
---

## 背景

#233 设计了 wt-create 内部自动 scan+pull 流程（步骤 5-7），当前只完成了步骤 1-4：
- ✅ 步骤 1-4：解析参数、拼分支名、创建工位
- ❌ 步骤 5：查 scan 结果 + source_family 匹配
- ❌ 步骤 6：根据 source 调对应的 pull 方法
- ✅ 步骤 7：raw-issue-pull 独立可用，但未集成到 wt-create 流程

另外 chat-inbox 来源的 raw issue 物化后没有调 issue-sync create 补 platform_ids。

## 方案

### `--source` 必填参数

```
freely wt-create --raw-key <key> --source <source> --skill <path> --slug <slug>
```

| --source 值 | 含义 | scan source_family | pull 方法 |
|------------|------|-------------------|----------|
| `chat-inbox` | freely.db chats 表 | `chat_inbox` | chat-inbox.py materialize |
| `platform` | GitHub/Gitee OPEN issue | 平台 API 扫描结果 | raw-issue-pull |

`--source` 和 `--skill` 一样是必填。AI 调用前需确定来源：读 scan 结果或查平台 issue 列表。

### wt-create 内完整 scan+pull 流程

```
wt-create --raw-key <key> --source <source> --skill <path> --slug <slug>
  │
  ├─ 1. 参数校验（--raw-key/--source/--skill/--slug 必填）
  ├─ 2. --skill 路径确定 prefix（fix-execution→fix, feat-execution→feature）
  ├─ 3. 拼接分支名
  │
  ├─ 4. 查 scan 结果中是否有 raw-{key}
  │   ├─ 有 → 提取 source_family
  │   │   ├─ source_family 与 --source 一致 → 继续步骤 5
  │   │   └─ source_family 与 --source 不一致 → 报错：
  │   │       "raw-{key} 在 scan 中的来源是 {source_family}，但传入了 --source {source}"
  │   └─ 没有 → 自动执行 task-lifecycle-scan.py
  │       ├─ 再查 → 有 → 继续步骤 5
  │       └─ 仍没有 → 拒绝：
  │           "raw-{key} 在 chat-inbox 和所有平台都未找到，请先创建 raw issue"
  │
  ├─ 5. 调 pull(raw-key, source) 物化到 docs/B1-docs/raw-{key}/
  │   ├─ source=chat-inbox → chat-inbox.py materialize + consume
  │   └─ source=platform   → raw-issue-pull（platform-adapter.py pull）
  │
  ├─ 6. pull 完成后检查 platform_ids
  │   ├─ chat-inbox 来源 → platform_ids 为空 → 调 issue-sync create 在所有已配置平台创建
  │   │   → platform_ids 写回 issue.md
  │   └─ platform 来源 → 检查各平台是否缺失
  │       ├─ GitHub 有 Gitee 没有 → issue-sync create gitee → platform_ids.gitee 写回
  │       └─ Gitee 有 GitHub 没有 → issue-sync create github → platform_ids.github 写回
  │
  ├─ 7. 创建双工位（test-pre-merge + fix/feature）
  └─ 8. sync-tooling
```

### pull 命令统一封装

当前 `_materialize_chat_if_needed` 只处理 chat-inbox，`raw-issue-pull` 只处理平台拉取。统一为一个内部函数：

```bash
_pull_raw_issue() {
  local raw_key="$1" source="$2"
  case "$source" in
    chat-inbox)
      # 现有 _materialize_chat_if_needed 逻辑
      ;;
    platform)
      # 调用 bin/raw-issue-pull --raw-key "$raw_key"
      ;;
  esac
}
```

### 关键差异：当前 vs 改进后

| | 当前 | 改进后 |
|---|------|--------|
| --source | 无 | 必填，AI 必须确定来源 |
| scan 匹配 | 无，只检查 chat-inbox + 目录存在 | 先查 scan，source_family 必须与 --source 一致 |
| 自动 scan | 无 | scan 结果没有 → 自动跑一次 scan → 再没有 → 阻塞 |
| pull 封装 | 散落在 `_materialize_chat_if_needed` + `raw-issue-pull` | 统一 `_pull_raw_issue(raw_key, source)` |
| platform_ids 补齐 | 无 | pull 后自动调 issue-sync create 补齐缺失平台 |
| 错误提示 | "未找到 issue" | "scan 来源是 X 但你传了 Y" / "所有来源都未找到" |

### AI 如何确定 --source

1. AI 拿到 raw-key 后，先查 scan 结果（`freely task-scan --json` 或读 scan JSON）
2. 找到对应 key 的 `source_family` → 确定 `--source`
3. 如果 scan 没有 → 检查平台 issue 列表 → 找到 `[RAW-{key}]` → `--source platform`
4. 如果都没有 → 先创建 raw issue（在平台上或 chat-inbox），再调 wt-create

### 成功标准

- `--source` 缺失 → clear error，提示 AI 先确定来源
- scan source_family 与 --source 不一致 → 报错，不建工位
- scan 没有 → 自动跑 scan → 再查 → 仍没有 → 拒绝
- pull 完成后 → docs/B1-docs/raw-{key}/issue.md 存在且 platform_ids 完整（所有已配置平台都有）
- chat-inbox 来源的 raw issue → platform_ids 不再为空
- 旧接口 `freely wt-create <branch>` 不受影响

## 改动范围

- `docs/system/workspace/scripts/worktree/wt-create`：增加 --source 必填 + scan 匹配 + pull 封装 + platform_ids 补齐
- `docs/system/workspace/skills/fix-execution/SKILL.md`：更新 wt-create 示例（加 --source）
- `docs/system/workspace/skills/feat-execution/SKILL.md`：更新 wt-create 示例（加 --source）

## 不改（后续 issue）

- #243 统一平台层（issue-sync 收拢 + platform-adapter 合并）
- #233 Source 3 平台扫描（task-lifecycle-scan.py 的 `_all_base_keys` 补全平台 API）

## 相关

- #233：原始 scan+pull 设计（步骤 5-7）
- #240：双工位创建
- #243：统一仓库平台层

- pre_tests_path: `docs/epics/source-param/verification/pre-tests.md`
- verification_artifact_dir: `docs/epics/source-param/code-reviews`
