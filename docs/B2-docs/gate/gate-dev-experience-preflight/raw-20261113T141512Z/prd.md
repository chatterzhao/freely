# PRD: status 只读视图空表降级
## Goal
空 agent_working 是正常「无活跃 agent」，不应让只读视图整体不可用。
## 实现
- status 系列入口设置只读标记；load_config 空表时降级为 info，不改写入路径。
## Handoff
先 RED 复现 rc=1，再改，再 GREEN。
