---
local_id: raw-20260616T111514Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260616T111514Z-A
platform_ids:
  github:
    issue_id: '2847'
    url: https://github.com/chatterzhao/freely/issues/2847
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-16T11:15:30Z'
updated_at: '2026-07-18T02:07:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

`freely` 脚本的 `write_config()` 用 `cat >"$cfg" <<EOF` 直接拼 TOML，完全绕过 `freely_config.py`。

### 子问题1: Shell变量注入
```bash
INTENT_FILE = "$intent"
```
如果 `$intent` 含双引号（如 `/path/to/"broken"/intent.md`），生成的 TOML 无效。

### 子问题2: 转义不一致
bash heredoc 不转义任何东西，而 `freely_config.py` 的 `_toml_quote` 会正确转义 `\` 和 `"`。两条路径产出不同格式的 TOML。

### 子问题3: 缺失10个posture/consent字段
`write_config` 只写 11 个 FREELY_* 字段，以下字段依赖事后 upsert 补充:
- FREELY_AUTONOMY_PROFILE
- FREELY_INTERACTION_POSTURE
- FREELY_APPROVAL_POSTURE
- FREELY_SAFEGUARD_GUIDANCE_POSTURE
- FREELY_RUNTIME_DECISION_POSTURE
- FREELY_MINIMAL_RISK_POSTURE
- FREELY_ACTIVATION_CONSENT_REQUIRED
- FREELY_ACTIVATION_CONSENT_STATUS
- FREELY_ACTIVATION_CONSENT_RECORDED_AT
- FREELY_ACTIVATION_CONSENT_RECORDED_VIA

init 后初始 config.toml 是不完整的，字段要等 upsert 才补上。

## 修复方向

`write_config` 应改为调用 `freely_config.py init-toml --value KEY=VALUE ...` 逐字段写入，单一序列化路径。
