---
candidate_id: C-20260704T004227Z-A
status: promoted
source_raw: raw-20260704T004227Z
created_at: 2026-07-04
milestone: M-20260704T004227Z-A
---

# Candidates

## C-20260704T004227Z-A: 修复 ACP bridge 启动链路三个 Bug

- candidate_format_version: v2
- title: |
  修复三个导致 agent-table 配置与实际执行不一致的 bug:
  (1) monitor-ai-acp.sh 未传 --acp-bin → bridge 默认用 claude-agent-acp
  (2) bridge 启动环境被父进程 ANTHROPIC_* 变量污染
  (3) agent-id grep -F 子串匹配导致 develop 上身份错判
- status: absorbed
- absorbed_into: I-20260704T004227Z-A
- decision_reason: |

  **Bug 1 — 主因**: monitor-ai-acp.sh 的 `_bridge_ensure_running()` (line 152) 不传 `--acp-bin`，
  导致 acp-bridge.py 默认用 `claude-agent-acp`。架构注释 (line 8) 直接写死 "→ claude-agent-acp"。
  `_ensure_acp_bridge_running()` 后来检查时，`.bin` 文件为空（monitor-ai-acp.sh 不写），
  `.tool` 文件匹配（写入了正确 tool name），健康检查通过 → 不重启 → claude-agent-acp 继续运行。

  **Bug 2 — 叠加**: 父进程 (Claude Code) 设置的 ANTHROPIC_MODEL=deepseek-v4-pro[1m] 等环境变量被
  所有 bridge 子进程继承。opencode slot 的 settings.json 无 env 字段来覆盖这些变量。

  **Bug 3 — 旁路**: agent-id grep 子串匹配 bug。

  三个 Bug 都涉及 bridge 启动/检查链路，合并为一个 candidate。

- next_action: B2 设计物化 I-* issue → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - monitor-ai-acp.sh `_bridge_ensure_running` 从 tool registry 解析并传入正确的 `--acp-bin`
  - `.bin` 文件被正确写入，后续 binary 变化可被检测到
  - bridge 启动前 unset ANTHROPIC_*/CLAUDE_CODE_*/AI_AGENT，只保留 slot-specific env vars
  - 启动后 session JSONL 中 model 与 agent-table slot 配置一致
  - opencode slot → opencode acp binary + deepseek-v4-flash-free 模型
  - claude slot → claude-agent-acp binary + settings.json env 字段中的模型
  - agent-id: develop 上 parser 为 manager_01
- promotion_gate: 三个修复代码完成，启动测试通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude-opus-4.7
  - mode: plan-subagent
  - summary: 审查 ACP bridge 启动链路的三个 bug，确认修复方案覆盖全部根因
  - verdict: pass
- promoted_issue_id: I-20260704T004227Z-A
- promoted_issue_path: docs/B2-docs/config/agent-table/raw-20260704T004227Z/issues/I-20260704T004227Z-A.md
- milestone: M-20260704T004227Z-A
- session_refs: []
