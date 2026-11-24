---
schema_version: '1'
local_id: raw-20261114T111702Z
kind: raw
phase_state: proposed
absorbed_into: ''
platform_ids:
  github:
    issue_id: '4654'
    url: https://github.com/chatterzhao/freely/issues/4654
    synced_at: ''
  gitee:
    issue_id: IKVBSU
    url: https://gitee.com/zhaoquan/freely/issues/IKVBSU
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-11-14T11:17:02Z'
updated_at: '2026-11-14T11:17:09Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: open
promoted_children: []
source_candidate: ''
completed_at: ''
closeout_note: ''
severity: P2
---

# fix: freely comment 引用未定义 PROJECT_ROOT，worker 通知静默失效

workflow_kind: fix

## fix: freely comment 引用未定义 PROJECT_ROOT，worker 通知静默失效

| Field | Value |
|-------|-------|
| local_id | `raw-20261114T111702Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-11-14T11:17:02Z |
| updated | 2026-11-14T11:17:02Z |

---

> **Freely 治理**：这是 raw issue `raw-20261114T111702Z`。实现前请用 `wt-create --raw-key 20261114T111702Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。

## 现象（吃狗粮实测，连续 3 次复现）

```
$ ./bin/freely comment --issue raw-<key> --file <body>
{ "github": {"status": "created"}, "gitee": {"status": "created"} }
/Users/.../docs/system/workspace/scripts/runtime/freely: line 25095: PROJECT_ROOT: unbound variable
```

平台评论**写成功了**，但命令尾部报 `unbound variable`；由于 `runtime/freely` 是 `set -u`，`cmd_comment()` 在写出 adapter 结果之后的那段「Notify active worker via ACP session/prompt」会中断。

## 根因（已定位）

- `runtime/freely:32` 只定义 `SELF_ROOT`（`SELF_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd -P)"`）；
- `PROJECT_ROOT` 只在 `:3707` 的某个函数内 `PROJECT_ROOT="$project"` 定义，**不是全局**；
- `cmd_comment()`（`:25027`）在 `:25095` 附近用 `${PROJECT_ROOT}` 拼 `agent_working` 的 sys.path 与参数，该作用域下 `PROJECT_ROOT` 未定义 → `set -u` 报错。

结果：`freely comment` 的「通知活跃 worker」步骤静默失效（`2>/dev/null || true` 吞掉了 python 失败，但 bash 的 unbound variable 仍打到 stderr）。写平台这一步不受影响，所以容易被忽略。

## 影响

- 表面无感（评论已创建），但 ACP worker 收不到评论通知；
- **对 `raw-20261114T101138Z`（dropped 收口自动写关闭理由）有依赖**：该方案要在关闭前自动写平台评论，若这条命令尾部报错，收口链路会带着非零/异常输出，可能被误判为失败。故建议在 #4653 的 P0 里判断是否并入。

## 期望

1. `cmd_comment()` 内统一改用已定义的 `SELF_ROOT`（或在该函数入口 `local PROJECT_ROOT="$SELF_ROOT"`），**等长替换、不新增行**——`runtime/freely` 正处 `check-runtime-size` 的 **27158/27158 行预算上限**，加行会判红。
2. 保持 `agent_working.agent_list_by_raw_key` 的调用语义不变。
3. AT：
   - `freely comment --issue <raw> --file <body>` 正常退出（rc=0）、stderr 无 `unbound variable`；
   - 平台评论仍创建成功；
   - 有活跃 worker 时 ACP 通知被实际调用（stub 断言）；
   - `check-runtime-size` 仍绿（行数不增）；
   - 基线（develop）红。

## 边界

- 不改 `freely comment` 的平台写逻辑、不改 adapter；
- 不放宽任何门禁；不撑爆 `runtime/freely` 行数预算；
- 不引入第二套根路径变量（复用 `SELF_ROOT` 单一真源）。

## 证伪 / 查重

- 现有 open 中 `#4589/#4570/#4539/#4455/#4428/#4363` 都是 `[I-20261101T031502Z-F]` 的 linked 残留（「讨论入口：issue comment / PR review / CI 进入 scan」），与「cmd_comment 引用未定义 PROJECT_ROOT」不同面，不重复；
- 不是 `~/.freely/versions` 安装态问题：dev 模式 `./bin/freely` 同样复现（真源即 `runtime/freely`）。
