# Tasks: ACP binary 自愈回写
- issue_id: I-20260718T035754Z-A
1. [x] 根因定位: config 空 → init 未运行/tool_adapter=direct → 无回写
2. [x] dev: bridge 启动时 PATH success 分支 upsert_config_key
3. [x] GREEN: 主仓实证 config 从空到 `/Users/zhaoyu/.nvm/.../claude-agent-acp`
