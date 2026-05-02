# Pre-tests: explicit-session-addressed-resume-governance

1. truth sources 明确区分：
   - `process alive`
   - `session resumable`
   - `resume target missing`
2. `codex` launcher 的默认 resume 路径必须显式携带 `SESSION_ID`；测试不得接受静默退回 `resume --last`
3. `codex exec resume [SESSION_ID] -` 的 prompt 续发路径必须保持可用
4. delegated continuation 不只保留抽象 `handoff://continuation`，还必须能写回当前 worker 的显式 resume target evidence
5. 本地 continuation re-entry 必须优先走 graceful preemption；若最终退回 hard kill，需留下可审计 evidence
6. `cc` / `cc-use-codex-cli` 继续使用 per-workcell `--session-id`，并被文档明确列为并发安全正向样本
7. `iflow` 当前 contract 必须被明确写成：
   - `--continue` = recent conversation
   - `--resume` = specific session file
   - 若 Freely 还未把它 materialize 成 workcell-scoped explicit target，则标记为未完全满足 canonical contract
8. `kiro-cli` 当前 contract 必须被明确写成：
   - `--resume` = current-directory most recent conversation
   - `--resume-picker` = interactive fallback
   - 当前不算并发安全的 canonical session-addressed resume
9. PTY input injection 仅能作为 fallback 解释，不得出现在默认 supervisor/runtime resume 路径
