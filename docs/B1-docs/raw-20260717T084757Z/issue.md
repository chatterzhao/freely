---
local_id: raw-20260717T084757Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260717T084757Z-A
platform_ids:
  gitee:
    issue_id: IK1RJV
    url: https://gitee.com/zhaoquan/freely/issues/IK1RJV
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-17T16:48:24+08:00'
updated_at: '2026-07-17T16:48:24+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 缺陷（多 agent 交接链路 SSE→session/* 环断点）
watchdog_sse.py 的 `def _get_agent_slot`（L474）位于 `if __name__ == "__main__"` 块（L462，内含 watchdog_run 阻塞死循环）之后——运行时永远执行不到定义。三处路由调用（reviewer L220 / manager L253 / worker L282）一触发即 NameError → SSE 循环断开重连 → 本次交接路由动作丢失。

## 实证
.freely/run/watchdog-sse.log：`routing to manager: needs decision …` 后紧跟 `SSE error: name '_get_agent_slot' is not defined, reconnecting in 8s`（2026-07-17 实抓）。df5161415（07-04）引入，潜伏至今——A2A SSE 的 Manager/Worker/Reviewer 路由每次实际触发都失败。

## 修复方向
def 移至 main 块之前；补一条"模块内所有被引用符号在 main 前定义"的静态断言测试；watchdog-sse.log 顺带补时间戳（本次排查因无时间戳无法直接判定错误归属实例）。
