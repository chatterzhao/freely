# PRD: ACP binary 自愈回写
- issue_id: I-20260718T035754Z-A
## Goal: daemon 首次启动后 config.toml 自动填入 ACP binary 路径
## 实现: bridge PATH fallback 成功后 upsert_config_key 回写
