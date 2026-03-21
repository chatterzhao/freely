# Pre-tests: explicit-session-addressed-resume-governance

- truth-source 明确区分：
  - process alive
  - session resumable
- `codex` 默认路径不再写成 `resume --last`
- `cc` 的 `session-id` contract 被明确视为并发安全基线
- 对 `iflow` / `kiro-cli` 当前 contract 有明确判定，不保持模糊
