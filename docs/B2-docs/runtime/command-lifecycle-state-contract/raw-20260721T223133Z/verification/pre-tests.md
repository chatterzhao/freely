# Pre-tests — command lifecycle state contract

- issue_id: `I-20260721T223133Z-A`
- phase: RED required
- target_lane: feature-local then test-pre-merge

## Historical-boundary acceptance

### META-000 feedback does not regain protected-branch local writes

- requirement: `feedback` 生成的平台 raw 载荷一次性包含完整 v1 flat schema；但命令仍不在 `develop` 直接创建或改写 `docs/B1-docs/**`。
- evidence: 从 feedback 结果读取/拉取的 frontmatter keys 与 `RAW_METADATA_FIELDS` 完全一致；受保护分支本地 issue 文档无写入。
- rationale: 历史 issue `raw-20260625T003331Z` 已证明 feedback 本地写文件会被 develop 保护机制阻止；本次只补齐创建载荷，不撤销平台-only 边界。

### META-000a wt-close is metadata read-only

- requirement: `wt-close` 可以读取 metadata 参与 phase/测试/所有权门禁，并通过既有平台 adapter 关闭平台 issue，但不得修改、补充、重排或重写 `docs/B1-docs/**/issue.md`。
- evidence: 执行前后 issue 文件字节内容和 hash 相同；平台关闭结果与本地 metadata 写入解耦。
- rationale: `wt-close` 的历史职责是验证、关闭工位和平台 issue；phase/absorption/drop 值必须由产生该事实的更早生命周期命令写入，不能把 closeout 当作修复 metadata 的机会。

### META-000b raw key recovery is all-platform and unique

- requirement: `raw_key` 是 raw 生命周期唯一主身份；`platform_ids` 仅是可丢失的缓存。缺失或不完整时，adapter 必须对每个已配置平台调用 `search_raw_issue(raw_key)`，每个平台均恰好解析出一个 issue 后才能开始关闭。
- cases:
  - 缓存完整有效：直接使用缓存，不执行多余查询。
  - 缓存缺失/部分缺失：对全部已配置平台重新唯一解析，再使用完整临时映射关闭全部平台。
  - 任一平台无处理器、零结果、多结果或关闭失败：失败闭合；不得开始本地分支/工位清理，不得写回 metadata。
- evidence: fake 双平台验证调用顺序为 `resolve missing → close every configured platform`；零/多匹配时 close 调用数为零。
- rationale: 平台 issue ID 是可恢复外部引用，不得反向成为 raw 生命周期的身份边界，也不得退化为任意单平台猜测。

## Unit acceptance

### META-001 canonical schema initialization

- requirement: 新 raw 物化后包含 v1 的 21 字段全集、固定顺序和显式初值。
- RED: 历史 `raw-issue-pull` 物化 sparse frontmatter，后续 writer 再按需插入字段。
- evidence: fixture frontmatter 与共享 schema 顺序逐项相等。

### META-002 semantic combinations

- requirement: proposed/absorbed/dropped 及 open/closed 组合按合同校验。
- RED: 当前无统一跨字段校验；`absorbed` 空目标可存在。
- cases:
  - proposed + empty relationship/completion values = pass
  - proposed + absorbed relationship = fail
  - absorbed + valid I-* + non-empty completed_at = pass
  - absorbed + existing project-relative canonical path + non-empty completed_at = pass
  - absorbed + no verifiable relationship = fail
  - dropped + non-empty completed_at/closeout_note = pass
  - dropped + empty completed_at or closeout_note = fail
  - platform_closed before absorbed/dropped = fail

### META-003 value-only transitions

- requirement: 生命周期事件只改变允许字段值，顶层字段集合和顺序保持不变。
- RED: 当前历史脚本仍会在 promotion/closeout 阶段按需插入 `promoted_children`、`absorbed_into`、`platform_state` 等字段；最终 schema 必须先通过历史写入点盘点确定字段全集。
- cases:
  - `feedback` 初始载荷已包含后续阶段确认需要的字段，包括空 `promoted_children`（若历史多子 issue 流程继续保留）
  - `issue-sync promote` 只更新既有 `promoted_children` 值，不提前改变 `phase_state`
  - `promote-finalize` 保持历史收口时机，只更新其拥有字段的值
  - `pr-merge-guarded` 的 raw 收口行为在对应历史 issue 审查完成前不得改变
  - `wt-close` 对 metadata 零写入
- evidence: 每个事件前后 keys/order 相等，diff 仅包含该历史阶段已确认拥有的值。

### PR-001 five-state classification

- requirement: absent/behind/equal/ahead/diverged 分类确定且与 remote 名无关。
- RED: 当前仅比较 local 与固定 github remote 是否相等。
- evidence: 临时 bare remotes 构造五态，逐一断言分类。

### PR-002 result normalization

- requirement: `created|updated|reused` 是成功，配置平台 `skipped|error` 是失败。
- RED: 当前 create 仅识别 `created`，push 采用 any-success。

## Integration acceptance

### META-101 wt-create preserves proposed

- requirement: raw pull 后执行 `wt-create`，phase 仍为 proposed，字段集合与顺序不变。
- RED: 当前 `_mark_raw_issue_absorbed` 无条件改成 absorbed。
- evidence: fake platform issue → pull → wt-create，比较前后 metadata。

### META-102 promotion preserves historical two-step ownership

- requirement: `promote` 原子记录 child/candidate 且 raw 保持 proposed/open；`promote-finalize` 从已登记 children 中选择首个可验证 `I-*`，一次写入主 ID、项目相对 canonical path、`completed_at` 并形成 absorbed/open；任一 finalize 输入无效则不写文件。
- RED: 当前写入器会按需新增 `promoted_children`，且历史文件可能只改 phase；新 schema 必须让两个阶段都只更新既有值。

### META-103 strict-new legacy-compatible

- requirement: v1 非法组合被拒；无 schema_version 的代表 legacy proposed/absorbed/dropped 可归一化读取，文件不被隐式重写。
- evidence: 新旧 fixtures 同时执行 scan/gate；比较 legacy 文件 hash。

### META-104 value-driven consumers

- requirement: scan/gate 不把存在但为空的字段视为成立。
- cases:
  - `absorbed_into: ''` 不能放行 absorbed
  - `canonical_issue_path: ''` 不能路由到 canonical issue
  - `platform_state: ''` 不能视为 closed
  - legacy `status` 仅在缺 phase_state 时作为兼容输入

### PR-101 existing PR local-behind-remote naming correction

- requirement: 本地提交领先远端（remote 相对 local 为 behind）时，先受控更新分支，再复用/更新已有 PR，最后 dry-run 通过。
- RED: 当前 merge dry-run 在 push 前因 head 不等退出。
- evidence: fake adapter 调用顺序必须为 observe → push → ensure-pr → dry-run。

### PR-102 idempotent equal rerun

- requirement: 分支 equal 且已有 PR 时不 push、不重复创建，返回 reused。

### PR-103 unsafe aggregate has no side effects

- requirement: 任一配置平台 ahead/diverged/error 时，在所有平台上均不执行 push/create/update。
- evidence: 双平台 fake adapter，断言副作用调用数为零并输出逐平台恢复信息。

### PR-104 dynamic platform aggregation

- requirement: 平台只从配置/registry 发现；所有配置平台都必须达到 equal + PR success。
- cases:
  - 两平台 absent/behind → 均 push + ensure PR → success
  - 一平台 equal/reused、一平台 behind/updated → success
  - 一平台 unsupported/skipped → aggregate failure

## End-to-end acceptance

### E2E-001 feedback-to-worktree lifecycle

```text
feedback/create platform issue with complete 21-field payload
→ raw-issue-pull materializes strict v1 and restores phase label
→ wt-create preserves proposed/open
→ promote records 1:N children without absorption
→ promote-finalize writes absorbed relationship + completed_at
→ controlled lifecycle close may set platform_state closed; wt-close remains metadata read-only
→ scan/gate reports valid
```

每个阶段验证固定 keys/order；阶段命令不得增删字段。

### E2E-002 existing PR reviewer-fix update

```text
create initial PR
→ add local reviewer-fix commit
→ rerun freely pr-create-guarded
→ every configured adapter updates branch
→ existing PR reused/updated
→ merge dry-run sees equal heads
```

禁止 raw push；证据必须包含逐平台分类、adapter action 和 aggregate success。

## Pre-merge acceptance

- 在 clean `test-pre-merge` 工位同步候选提交。
- 运行 metadata 单元/集成套件、PR adapter 五态套件、相关 lifecycle/scan/gate 回归。
- 对修改 Shell 执行 `bash -n`，对 Python 执行既有项目测试入口。
- `.freely/run/test-gate.env` 必须绑定完整候选 commit。

## Real-environment acceptance

- 本修复落到 `develop` 后，将其受控集成到暂停的 agent-identity continuation。
- 在该 continuation 重跑 `freely pr-create-guarded`。
- GitHub PR `#4069` 必须由 adapter 更新到本地 reviewer-fix commit，且不得建议或使用 raw `git push`。
- 若配置包含其他平台，必须给出该平台明确成功终态；任何配置平台失败则 real-environment 不通过。

## Evidence policy

每项证据记录：完整 commit、命令、退出码、逐平台结果、测试数量及日志路径。登录 shell 缺依赖属于环境证据，不可替代实际测试结果，也不得删除。
