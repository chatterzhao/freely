# Candidates - 20260402-1912--protected-branch-merge-receipt-hardening

## C-20260402-1912-A

- candidate_format_version: `v2`
- title: Protected-branch merge receipt hardening
- problem: `protected-branch-hook-bypass-breakglass-governance` 已经把 break-glass whitelist、guarded completion 和 receipt audit 的 phase-1 contract 合入 canonical `develop`，但 closeout 后仍暴露出一个更窄的 residual hardening slice：guarded completion handshake 仍偏软，`governance-check` 还没有验证 merge receipt trailer 与 break-glass ledger 的字段一致性，而 merge-gate 的 staged/touched relevance 边界也仍有误放宽风险。当前根目录 staged patch 证明这类问题还在被人尝试处理，但该 patch 同时混入了对已吸收 watchdog 修复的回退，不能直接当 canonical answer。
- why_now:
  - canonical `develop` 已经 close out 原 break-glass owner，再继续往那条 owner 里塞 residual hardening 会破坏边界
  - 根目录 `develop` 当前出现未归属 staged 改动，说明这条 follow-on 如果不物化，后续仍会以 dirty root patch 的形式反复出现
  - staged patch 中对 `pr-merge-guarded` / `governance-merge-gate` / receipt tests 的调整方向互相掺杂，必须先收成一个明确 owner 再决定实现
- acceptance_criteria:
  - 证明 follow-on 仅覆盖 `merge_completion_only`、handshake hardening、receipt/ledger parity audit 和相关 regression coverage
  - 明确根目录 staged patch 中哪些变化是 residual hardening signal，哪些是应直接丢弃的 regression 或 unrelated revert
  - 给出 `pre-merge-commit` break-glass 短路的 tighter contract，确保不扩张到初始 clean merge
  - 给出 guarded completion handshake 的更硬 runtime contract，并明确最小测试面
  - 给出 `governance-check` 对 protected-branch merge receipt trailer 与 ledger field parity 的审计方向
  - 给出 `governance-merge-gate` staged/touched relevance 的 regression boundary，避免 sibling candidate 或 staged-only owner 再次被误分类
  - 明确 watchdog repo-root resolution 不属于这条 owner，且不得通过此 owner 回退 `e506982`
- promotion_gate:
  - 不 reopen `I-20260402-0020-A`
  - 不把 root `develop` staged patch 直接当 canonical solution
  - 不把 watchdog revert 混进 merge-governance hardening
  - 不为修 staged false negative 而移除已有 receipt / watchdog / merge tests
- open_questions:
  - guarded completion handshake 的最小 machine-readable receipt / state 应落在哪个 artifact 面
  - parity audit 应只校验 `develop` HEAD merge，还是要覆盖更广 ancestry
  - `governance-merge-gate` 是否还需要 staged-view 能力，还是应该改成别的 evidence 连接方式
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: 这是已完成 break-glass owner 的 follow-on hardening，不该复用广义旧候选，也不该吸收 unrelated watchdog revert。
- decision_reason:
  - canonical `develop` 已完成 break-glass policy owner，follow-on 应该更窄而不是更宽
  - dirty root staged patch 只能证明“还有 residual signal”，不能替代 owner boundary
  - 把 watchdog revert 和 merge receipt hardening 拆开，才能避免再次把 unrelated regressions 混入 protected-branch 修复
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260402-1912-A`
- promoted_issue_path: `docs/B2-docs/ibm/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - this candidate materialized as `I-20260402-1912-A`
  - keep the owner focused on receipt parity, completion-only boundary, and staged regression coverage
  - do not reopen broad break-glass governance or absorb watchdog revert through this lane
- revisit_trigger:
  - protected-branch merge tooling again needs manual explanation around completion-only bypass
  - `governance-check` still accepts receipt/ledger mismatches
  - root `develop` again accumulates merge-governance residual patching without an owner
