# Implementation Decision Note
- issue_id: I-20261103T132556Z-A
- decision: 两层 session 路由（客户端入站 positively-mismatched 过滤为权威 + bridge 定向投递为纵深防御 fail-open 回退）+ `bypassPermissions` 裸默认改显式 opt-in（`CLAUDE_CODE_PERMISSION_MODE` 保持权威）
- why_this: 单 bridge 向所有客户端广播 server 通知、客户端零 session 校验，使 worker A 的 `agent_message_chunk` 写进 B 的 stdout 且 B 以 allow 越权代答 A 的权限请求——已知唯一「并发正确性 + 权限越界」双料缺陷。客户端确定性地知道自身 session，是最可靠的过滤点。
- alternatives_considered: ①每 session 一个 bridge/连接（issue 方案 4）——常驻进程数暴涨（≥6）、与存量设计冲突，否决；②bridge 对未知 session 直接丢弃（issue 方案 1 字面）——U6 前提未验证、会丢消息，收窄为 fail-open 广播；③直接翻 `bypassPermissions` 裸默认无 opt-in——未配置部署会 hang（退化），收窄为权威 env + 显式 opt-in；④仅在 bridge 层修——bridge 无可靠 session 归属，不能作为唯一正确性来源。
- boundary_non_goals: 其余会话协商 / prompt 分派 / set_mode / server 存活 / stdout 解析逻辑未改；`docs/epics-map.svg` 未改（复用 `acp/cross-tool-session`）；`acp_bridge_v2.py`（SDK 版，当前不存在）不在本轮范围；cc 非 ACP 路径的 `--permission-mode bypassPermissions` 未动。
- residual_risk: ①U6 真实流量（session/update 是否总带 sessionId）本机无法抓取（无 SDK/server/平台凭证），故所有未知/缺失路径取 fail-open，即使 U6 不成立也不丢消息——代价是回退广播仍会把 A 的消息发到 B 的 socket，但 B 的客户端入站过滤会丢弃，正确性不受影响；②真机多 worker 端到端未跑，按 issue 验收标准用隔离 mock（真实真源模块 + develop 基线快照）替代；③`acp_bridge_v2.py` 若将来上线需复核两层路由是否同样生效；④「未知 session 丢弃」的收紧留待 post-merge 验证 U6 后再评估，本轮不做以避免消息丢失。
- verification: AT-001 develop 基线快照 RED `9 ok / 10 failed` → 工位 GREEN `19 ok / 0 failed`；`test-prompt-manifest-integration.py` 双树 PASS；4 个 cc 预存红测试 worktree 与 develop 基线退出码/输出逐字节一致（仅 mktemp 随机后缀与绝对路径前缀不同，归 #4151）；`check-epics-map` 16 epics / 206 stories aligned。
- self_bootstrap_findings: 复核运行时路径时发现 `acp-bridge.py` 顶部在 acp SDK 可 import 时会 execv 到不存在的 `acp_bridge_v2.py`——本机 SDK 不可用故走 legacy，测试显式 `FREELY_ACP_USE_SDK=0` 固定；该 execv 分支本身非本 issue 覆盖的缺陷（且 SDK 路径当前不可达），未新建 raw issue。未发现其他未被 open issue 覆盖的新缺陷。
