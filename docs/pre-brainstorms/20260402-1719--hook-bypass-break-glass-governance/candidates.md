# Candidates - 20260402-1719--hook-bypass-break-glass-governance

## C-20260402-1719-A

- candidate_format_version: `v2`
- title: Hook bypass break-glass governance and audit
- problem: Freely 当前依赖本地 Git hook 和 merge gate 保护 `develop`，但没有冻结“何时允许 break-glass bypass、何时绝对禁止”的 canonical 规则，也没有事后审计 protected-branch merge 是否经过受控 gate path。结果是 agent 在 gate 误判或 merge completion friction 出现时，可能直接用 `--no-verify` 完成 merge，并把个人判断误当成合法豁免。
- why_now:
  - 狗粮链路已真实出现 develop-bound `--no-verify` bypass，而不是抽象风险
  - 现有文档强调启用 `.githooks`，但没有把 break-glass 白名单、证据与补救动作写成唯一词典
  - 仅靠本地 hook 无法形成绝对硬防线，必须补上 policy + receipt + audit 三层
- acceptance_criteria:
  - 明确 protected branch gate bypass 默认违规，只有显式白名单场景允许
  - 明确 break-glass 规则的分层落点：`CONSTITUTION`、`LAWS`、`AGENTS`、能力真源、skills
  - 定义允许 bypass 的最小场景词典，并明确未列入者一律禁止
  - 定义每个允许场景的前置条件、最小证据、补救要求与收尾动作
  - 明确 hook/merge 真源必须说明“client-side hook 不是绝对硬防线”
  - 给出 `merge-guarded` conflict completion path 的收紧方向
  - 给出 `governance-check` 对 protected-branch bypass 的事后审计方向
  - 明确这次已发生的 bypass 不构成合法豁免
- promotion_gate:
  - 不把“agent 自己确认是 false negative”当成合法 bypass
  - 不把 break-glass 定义留在 skill 或临时会话解释里
  - 不只写政策文本，必须给出能力真源和 audit 接点
  - 不借此回退整个 ownership feature；优先 forward-fix governance hole
- open_questions:
  - bypass receipt 最小真相应是 commit trailer、artifact file，还是双写
  - `merge-guarded` 是否应该生成受控 completion receipt 并接管冲突后 commit
  - `governance-check` 是否只检查新 merge 还是检查全部受保护分支 head ancestry
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `supports`
    note: 当前缺口不是“有没有 hook”，而是 Git 可绕过、文档未冻结 break-glass、merge completion path 无受控收尾、且事后无审计。
- decision_reason:
  - 这是 Freely 自举暴露出的真实治理缺口，继续靠人工默契会反复复发
  - 原 feature merge 本身承载有效能力，不应因 bypass hole 直接整体撤销
  - 更合理的处置是前向修复治理、记录违规、并给 future merge 加 receipt/audit
- priority: `P0`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `pending://issue-materialization`
- promoted_issue_path: `pending://issue-materialization`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - 冻结 break-glass layering 与 allowed-scenario dictionary
  - 判定这次 bypass 的 canonical 处置方式和留痕面
  - materialize follow-on owner，补 `merge-guarded` completion path 与 `governance-check` bypass audit
- revisit_trigger:
  - 任何 develop-bound merge 再次需要人工解释是否可 `--no-verify`
  - hook/gate false negative 仍只能靠人工绕过收尾
  - protected-branch merge 缺少 machine-readable bypass evidence
