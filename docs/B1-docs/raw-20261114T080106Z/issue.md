---
schema_version: '1'
local_id: raw-20261114T080106Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261114T080106Z-A
platform_ids:
  github:
    issue_id: '4645'
    url: https://github.com/chatterzhao/freely/issues/4645
    synced_at: ''
  gitee:
    issue_id: IKVB18
    url: https://gitee.com/zhaoquan/freely/issues/IKVB18
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/platform/issue-sync-entrypoint/raw-20261114T080106Z/issues/I-20261114T080106Z-A.md
last_synced_comment_at:
  github: '2026-11-14T08:42:45Z'
  gitee: '2026-11-14T08:42:45Z'
hash: ''
created_at: '2026-11-14T08:01:06Z'
updated_at: '2026-11-14T08:42:49Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261114T080106Z-A
source_candidate: ''
completed_at: '2026-11-14T08:42:44Z'
closeout_note: ''
severity: P2
---

# fix: 安装态自检入口缺失，goal 写的命令跑不通

workflow_kind: fix

## fix: 安装态自检入口缺失，goal 写的命令跑不通

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T080106Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T08:01:06Z |
| updated | 2026-11-14T08:01:06Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T080106Z`。实现前请用 `wt-create --raw-key 20261114T080106Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（吃狗粮实测）

用户要求「前面实现了的要进行打包安装……不然自己吃自己狗粮，可能吃到过期的」，我按 `.freely/goal-arch-debt.md` 核对安装态时撞到：

```
$ ./bin/freely install-state-check --json
[ERROR] unknown command: install-state-check
```

但 goal 第 22 行把「`install-state-check --json` → `ok:true`」写成**吃狗粮前提**，且 `docs/system/workspace/scripts/tests/test-install-state.py` 也引用 `install-state-check.py` CLI。

实测真实入口：
- `python3 docs/system/workspace/scripts/quality/install-state-check.py --json` → `ok:true`，`project_head = packaged_from = bbe3baf66`；
- `docs/system/workspace/scripts/runtime/freely:24817` 只在 `cmd_doctor()` 内部调用它，**没有独立的 `install-state-check)` 分派**。

也就是说：能力（自检脚本）存在，但**文档声明的调用方式不存在**，`bin/freely` 也没有对应一等入口。执行者按 goal 抄命令会拿到 `unknown command`，无法确认「是否吃到过期安装态」——正是用户担心的那个风险面。

## 影响

- 每轮合并后 `pr-merge-guarded` followthrough 自动重打包激活（goal:22、:91 已说明），本次 `./bin/freely-package --version auto --activate` 也返回「installed state already matches HEAD bbe3baf66; nothing to do」，**当前没有过期**；
- 但缺少一个「按 goal 抄就能跑」的自检命令，等于把「吃狗粮前提」变成一句无法验证的断言；
- 若某天自动打包失败，执行者按文档自检会得到 `unknown command`，可能误判为「命令变了」而不是「安装态过期」。

## 期望（方向，方案由 B1 决策）

1. 让「安装态自检」成为 `./bin/freely` 的一等子命令（或等价的、goal 可照抄的入口），输出与现有脚本一致的 JSON（`ok / project_head / active_version / packaged_from / command_path`）；
2. 同步修正 goal、commands.md 等文档中对该命令的写法，使「文档写的命令 = 实际能跑的命令」；
3. 自检应能明确区分「安装态与 develop 不一致」并给出修复命令（`freely-package --version auto --activate`）。

## 证伪 / 避免重复立项

- `IKTSRS / raw-20261108T134701Z`（`bin/freely` 注释承诺 `freely install` 与 `@freely-dev-path`，命令从未实现）**不同面**：那条讲安装/卸载与 zshrc 标记，本条讲**自检入口与文档一致性**，不重复；
- `test-install-state.py` 只测脚本存在与 doctor 输出，未覆盖「goal 声明的 CLI 能否执行」；
- 不改 `cmd_doctor()` 现有行为、不改打包逻辑、不放宽任何门禁。

## 边界

- 不改 `freely-package` 的幂等/激活语义；
- 不为凑命令而复制第二套自检真源（必须复用 `quality/install-state-check.py`）；
- 注意 `docs/system/workspace/scripts/runtime/freely` 有 **27158 行预算**，若在其内加分派必须同步压缩或走薄投影，不得撑爆 `check-runtime-size`。

## 验收（AT，带基线红）

1. `./bin/freely install-state-check --json` 返回 `ok:true` 且与 `install-state-check.py --json` 字段一致；
2. 安装态与 develop 不一致时返回非 0 / `ok:false`，并给出 `freely-package --version auto --activate`；
3. goal / commands.md 中的命令写法与实际可执行入口一致（静态断言）；
4. `test-runtime-split.py` 的 budget 断言仍绿；
5. 基线（develop）红。

### comment-20261114T084245Z
- source: system
- event: promote_finalized
- children: ["I-20261114T080106Z-A"]

拆解为以下任务:
1. [I-20261114T080106Z-A](will-be-updated)
