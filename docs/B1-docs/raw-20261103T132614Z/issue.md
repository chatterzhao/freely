---
schema_version: '1'
local_id: raw-20261103T132614Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261103T132614Z-A
platform_ids:
  github:
    issue_id: '4154'
    url: https://github.com/chatterzhao/freely/issues/4154
    synced_at: ''
  gitee:
    issue_id: IKSPQ9
    url: https://gitee.com/zhaoquan/freely/issues/IKSPQ9
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261103T132614Z/issues/I-20261103T132614Z-A.md
last_synced_comment_at:
  github: '2026-11-10T11:26:24Z'
  gitee: '2026-11-10T11:26:24Z'
hash: ''
created_at: '2026-11-03T13:26:14Z'
updated_at: '2026-11-10T11:26:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261103T132614Z-A
source_candidate: ''
completed_at: '2026-11-10T11:26:23Z'
closeout_note: ''
---

# refactor: 收口契约常量与 raw key 多副本

workflow_kind: feature

## 根因
同一定位符 / 枚举 / 协议在不同层各自维护一份，缺单一来源与自动比对。漂移不会编译失败、不会测试失败，只会「行为莫名不对」。

## 证据
- 工具注册表路径 2 版（副本已错）：真实位置 `docs/system/workspace/tools/tool-registry.toml`；`freely:46` 正确，而 `bin/deploy-skills:72`、`bin/ensure-acp-binary:8`、`freely:21170` 指向不存在的 `scripts/runtime/tool-registry.toml` → 三处静默降级（deploy-skills 回退 `tools="claude"`；ACP 工具初始化整段跳过只留一条 warn）。
- 桥接契约 4 份，只单向校验：`public/freely-probe-bridge-manifest.json`、`src-tauri/src/bridge_manifest.rs:1-13`（唯一校验 `:31-56`，只断言 Rust ↔ public JSON）、`src/frontend_probe_v0/bridgeManifest.ts:1-21`、`bridgeBindings.ts:7-11`（TS 与 public JSON 无任何自动化比对）。事件枚举不对称：`contracts.ts:71-102` 声明 8 种，`event_kind.rs:2-9` 只有 6 种（缺 `GovernanceDecisionRecorded` / `RecoveryStatusChanged`，且无 `Other` 兜底）→ 前端两段 UI 分支永远拿不到数据；`eventId` 语义失效（`bridge_logic.rs:52` 每命令自增、`event_payload.rs:23-26` 全事件共用）→ `AppShell.tsx:322,451,519` 的 `key={event.eventId}` 重复。
- 平台写 3 套并存：`bin/issue-sync:4-6` 自称 `the ONLY code that touches platform APIs`，实际 `platform-adapter.py:703-704`（`register(GitHubHandler())` / `register(GiteeHandler())`）、`bin/pr-review-guarded:136`、`bin/issue-sync-bootstrap:24`、`wt-close:917`、`pr-merge-guarded:272,276,285,614,690` 都在直连 `gh` / 第二套 Gitee 客户端。分叉后果具体：label（`issue-sync:310` 传 `kind/*,phase/*`，而 `platform-adapter.py:728-737` `create_issue(local_id, title, body)` 签名无 labels → 标签缺失，所有基于 label 的治理门失效）。
- raw key 3 套正则：`bin/wt-create:242-256` 接受两种格式且只告警不规范化，下游 7 处只匹配 `T...Z`（`freely:6050,13155,13330,13425,19078`、`hooks/pre-commit.sh:29`、`owner_lane.py:32`），`bin/worktree-common.sh:56-63` 是第三套 → legacy 格式建工位后 `raw_key=""`，`freely:11173-11175` 拼出 `docs/B1-docs/raw-/issue.md`，`owner_lane.py:151-154` 报 `raw_key_unresolved` 使 daemon fail-closed 拒启动。
- 错误模型 4 套：`Result<T,String>` 无错误码（`lib.rs:34,48`）/ `CommandAck.ok` 恒 true（`bridge_logic.rs:111-112`，未知命令也 ok）/ 字符串 `"ok"|"fail"` + `|| true`（`issue-sync:314,317,322,325-334`）/ `{"status":"error"}`（`platform-adapter.py:221-222` 的 `{"status": "error", "error": ...}`）/ `SystemExit`（`gitee-issue.py:44,50-55`）。
- 文档 / 脚本根 2 套：`$SELF_ROOT/docs`（75 处）vs `$project/docs`（14 处，如 `freely:315,318,374,20582`）→ manager 用 develop 版脚本，worker worktree 用自己分支版脚本，同一控制面里跑两代实现。
- 注：`platform-adapter.py` 的全部引用已在 HEAD `9bcafa45f` 重取（旧报告行号因 +64 行提交整体漂移），本条目内不再有偏移注记。

## 影响
改契约 / 加事件需要手工同步 6~8 处，漏一处就产生上述漂移。这是本报告里单位成本最高的一类债务，且路径、raw key、事件枚举三类副本都已被证实会产生实际错误行为（不是理论风险）。

## 修复方案
1. `tool-registry.toml` 路径改为单一常量（`bin/deploy-skills:72`、`bin/ensure-acp-binary:8`、`freely:21170` 三处），启动时断言文件存在，缺失即失败而非降级。
2. raw key 在 `wt-create` 入口统一规范化为 `YYYYMMDDTHHMMSSZ`，shell 侧复用已存在的 `runtime/raw_key_canon.py`；下游 7 处匹配改调同一函数。
3. 桥接契约把 `public/...json` 降级为构建产物，加一条 TS↔Rust 双向测试（顺带校验事件枚举集合与 `payloadShape`）。
4. `issue-sync` 的平台写路径收口到 `platform-adapter.py`（与 #4149 同一改动），`create_issue` 增加 labels 参数；其余直连 `gh` 的调用点一并迁走或明确登记为例外。
5. 错误模型定一种（建议 `Result<T, {code,message}>`），`CommandAck.ok` 按真实结果取值。

## 验收标准
- RED：把 `docs/system/workspace/tools/tool-registry.toml` 临时改名后运行 `bin/deploy-skills`，断言报错退出；当前回退到 `tools="claude"` 继续。
- RED：用 legacy raw key（无 `Z` 后缀）执行 `wt-create`，断言要么被规范化后成功、要么明确拒绝；当前产出 `raw_key=""` 并让 daemon 拒启动。
- GREEN：`grep -rn "scripts/runtime/tool-registry.toml" bin/ freely` 无命中。
- GREEN：新增的 TS↔Rust 契约测试在删掉 `event_kind.rs` 任一事件变体时失败（当前无此守护）。

### comment-20261110T112623Z
- source: system
- event: promote_finalized
- children: ["I-20261103T132614Z-A"]

拆解为以下任务:
1. [I-20261103T132614Z-A](will-be-updated)
