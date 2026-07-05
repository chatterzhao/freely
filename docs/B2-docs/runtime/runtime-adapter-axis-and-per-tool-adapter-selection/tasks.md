# Tasks: runtime-adapter-axis-and-per-tool-adapter-selection

1. 在 runtime config 中引入 first-class `AI_TOOL_ADAPTER_POLICY` 与 `AI_TOOL_ADAPTER` truth，并保持 current tools 默认 `direct` policy。
2. 为 current tools 冻结 default adapter 与 supported adapter metadata。
3. 将 launch dispatch 从 `tool -> launcher` 重构为 `adapter -> tool implementation`。
4. 保持 continuity / recovery / session evidence writeback 继续走现有 canonical surfaces。
5. 为未实现 adapter 建立显式 unsupported/fail-fast contract。
6. 更新 status / introspection surface 暴露 adapter truth 与 policy truth。
7. 增加 focused runtime tests，锁住 direct no-regression 与 unsupported-adapter behavior。
8. 冻结 adapter selection 语义：同工具保留当前 adapter/policy truth，跨工具才回落到目标工具默认 policy，并为显式 adapter/policy override 预留稳定入口。
9. 提供最小受管 mutation command，让 runtime config 能在不手改 `.freely/config.env` 的前提下切换 tool + adapter/policy。
