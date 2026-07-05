# Refactoring Tasks: chat intake → issue unification

## Categories

- **[KEEP]** = 不改变，逻辑和路径都不变
- **[CHANGE]** = 逻辑保留，路径/存储改变
- **[NEW]** = 从零构建
- **[REMOVE]** = 删除
- **[GATE]** = 门禁逻辑需新增

---

## 1. 存储层

### [NEW] 1.1 创建 docs/issues/ 目录结构
- `.scan-state` 文件：`{last_scan_at: ISO8601}`
- `ISSUES.md` 缓存索引（脚本维护）
- `raw-{key}/issue.md`：frontmatter 元数据 + 正文 + ## Comments
- `I-{key}/issue.md`：frontmatter 元数据 + 摘要 + ## Comments
- 内部格式：YAML frontmatter，## Comments 下 ### comment-{local_id} 条目

### [NEW] 1.2 脚本 `bin/issue-index`
- 扫描 `docs/issues/*/issue.md` 的 frontmatter
- 生成/更新 `ISSUES.md` 缓存索引
- 增量模式：读 `.scan-state.last_scan_at`，只处理 mtime 更新的文件
- 全量模式：遍历所有 issue.md，重建索引

### [REMOVE] 1.3 废弃 .freely/intake/
- 迁移脚本 `bin/issue-migrate-intake`（一次性）
- 验证后 `rm -rf .freely/intake/`

---

## 2. chat 命令

### [CHANGE] 2.1 `freely chat` 命令
- **当前**：`freely chat "msg"` → `write_intake_item()` → `.freely/intake/<id>/message.txt`
- **改为**：`freely chat "msg"` → chat-routing skill 判断 → 创建 raw issue 或追加评论到 `docs/issues/<id>/issue.md`
- 保留：`--message-file`、runtime bootstrap check、interruption dispatch
- 新增：`--issue <id>`（指定已有 issue）、`--urgent`（紧急标记）

### [CHANGE] 2.2 `freely intake chat/claim/resolve/status` 命令
- **当前**：写入 `.freely/intake/`，claim/resolve 修改 meta.env 状态
- **改为**：写入 `docs/issues/`，claim/resolve 修改评论 `###` 的元数据行状态
- `intake status` → 改为读取 `ISSUES.md` 索引，汇总各 issue 的未处理评论数

### [CHANGE] 2.3 `write_intake_item()` 函数
- **当前**：创建 `.freely/intake/<id>/` 目录 + `message.txt` + `meta.env`
- **改为**：创建 `docs/issues/raw-{key}/` 目录 + `issue.md`，或追加评论到已有 issue.md

### [KEEP] 2.4 `submit_human_frontdoor_message()` 函数
- 不做实质改动。内部的 `cmd_intake_chat` 调用会被 CHG 2.2 覆盖。

---

## 3. scan 脚本

### [CHANGE] 3.1 `task-source-scan.py: scan_intake()`
- **当前**：扫描 `.freely/intake/` 目录
- **改为**：扫描 `docs/issues/raw-*/issue.md`（未关联 candidate 的 raw issue）
- 输出：restart_point=pre_brainstorm，source_family="raw_issue"

### [NEW] 3.2 `task-source-scan.py: scan_linked_issues()`
- 扫描 `docs/issues/I-*/issue.md`
- 有新评论（`last_synced_comment_at` 后有新 `###`）→ restart_point=cleanup

### [CHANGE] 3.3 `task-source-scan.py: build_payload()`
- `scan_intake()` → 改为 `scan_raw_issues()`（CHG 3.1）
- 新增 `scan_linked_issues()` 调用（NEW 3.2）
- source_families 总数从 6 变为 7（移除 intake，新增 raw_issue + linked_issue）

### [CHANGE] 3.4 `task-source-scan.py: scan_external_github/gitee()`
- **当前**：下载平台 issue 后直接在 scan 结果中返回
- **改为**：下载后先写入 `docs/issues/raw-{key}/issue.md`（如果本地还没有），再返回 scan 结果
- 平台 raw issue → 本地 raw issue 的一一对应

### [KEEP] 3.5 `scan_pre_brainstorms()`, `scan_milestones()`, `scan_progress()`
- 不改变。

---

## 4. chat-routing skill

### [NEW] 4.1 chat-routing skill 脚本
- 输入：用户消息文本
- 输出：{action: "new_issue" | "comment", target: <issue_id>}
- 快速路径：正则匹配 issue 引用（#123, raw-xxx）
- AI 路径：调 AI 做语义匹配（读 ISSUES.md 索引中的 title + status）
- 挂载为 `docs/system/workspace/skills/chat-issue-routing/SKILL.md`

### [CHANGE] 4.2 interruption-manager-handler
- **当前**：读 `.freely/intake/`，做 fast-path 分类
- **改为**：读 `docs/issues/` 中新评论的 `###` 条目，做同样的分类
- 分类逻辑本身不变

---

## 5. sync 脚本

### [NEW] 5.1 `bin/issue-sync` 脚本
- `issue-sync create <local_id>`：创建平台 issue → 回写 platform_id
- `issue-sync comment <local_id>`：推送未同步评论 → 回写 comment_id
- `issue-sync update <local_id>`：更新平台 issue body
- `issue-sync close <local_id>`：关闭平台 issue
- `issue-sync pull`：从平台拉取新评论
- `issue-sync status <local_id>`：查看同步状态
- `issue-sync rebuild <local_id>`：从本地强制重建平台 issue

### [NEW] 5.2 平台适配器
- github 适配器：`docs/system/workspace/scripts/sync/github-adapter.py`
- gitee 适配器：`docs/system/workspace/scripts/sync/gitee-adapter.py`
- 统一接口：create_issue / update_issue / close_issue / add_comment / pull_comments

---

## 6. hook / gate

### [GATE] 6.1 governance-merge-gate: raw→C key 链校验
- 新增：candidate 如果是 promoted 状态，必须有对应的 raw issue（共享 date-time key）
- 校验逻辑：C-{key}-{split} → issue_key 的前段必须匹配某个 raw-{base_key}
- 例外：如果 raw issue 是平台原始 issue（非本地 chat 创建），不强制本地有 raw 目录

### [GATE] 6.2 pretests-gate: issue 元数据校验
- 新增：linked issue (I-*) 的 `platform_ids` 非空
- 新增：`primary_platform` 存在
- 新增：`sync_state` = synced（merge 到 develop 前）

### [GATE] 6.3 pre-merge-commit hook: sync check
- 新增：merge 前检查 linked issue 是否已同步到平台
- 未同步 → 警告（不阻断，网络可能不可用）

### [KEEP] 6.4 现有 hook/gate
- pre-commit.sh、pre-push.sh、pre-merge-commit.sh 的主体逻辑不改变
- governance-merge-gate 和 pretests-gate 的现有校验不改变

---

## 7. 文档

### [CHANGE] 7.1 AGENTS.md
- 已更新：IBM Framework 路由章节
- 待更新：chat 插话→issue 路由的引用

### [CHANGE] 7.2 ibm-framework.md
- 已更新：新增 Issue 存储与平台隔离章节
- 已更新：B1 信号进入路径

### [CHANGE] 7.3 PROJECT_INTENT.md
- 已更新：B1_IBM/B2_IBM 术语

### [CHANGE] 7.4 LAWS.md §2A/§2B
- 待更新：source routing 规则（intake → raw issue）
- 待更新：IBM 边界规则（B2_IBM 命名）

---

## 8. 废弃项

### [REMOVE] 8.1 .freely/intake/ 目录
- 废弃 `.freely/intake/<id>/message.txt` 结构
- 废弃 `.freely/intake/<id>/meta.env` 结构

### [REMOVE] 8.2 intake 相关的 runtime 状态
- 废弃 `write_intake_item()` 的旧实现
- 废弃 `cmd_intake_claim/resolve` 的旧 meta.env 操作路径
- 废弃 `intake_pending_signal_file`（改用 urgent comment 检测）

---

## 9. 关键不变项

### [KEEP] 9.1 治理流程
- B1_IBM: Input → Brainstorm → Milestone（不变）
- B2_IBM: Input → Brainstorm → Map（不变）
- candidate lifecycle: proposed → needs_research → blocked → promoted/absorbed/dropped（不变）
- issue phase_state: in_b2_ibm → done_b2_ibm → in_dev → blocked_dev → in_verification → completed（不变）

### [KEEP] 9.2 现有目录
- docs/pre-brainstorms/（不变）
- docs/epics/（不变）
- docs/progress/（不变）
- docs/system/workspace/（不变）

### [KEEP] 9.3 运行循环
- three-loop 路由（不变）
- supervisor/worker/lead 三角色（不变）
- auto-loop signal intake / patrol（不变，只改 scan 的源）
