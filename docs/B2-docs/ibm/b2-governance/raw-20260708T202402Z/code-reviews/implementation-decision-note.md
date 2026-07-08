# Implementation Decision Note
- issue_id: I-20260708T202402Z-A
- decision: 恢复旧scan的STATION_ACTIONS(14站)+_detect_station()+_build_sync_batch(指纹去重)+_render_next_action(两级渲染)，保留新scan的argparse、platform-adapter、A2A集成。
- why_this: 旧scan的两级[manager]/[worker]委派模式是Manager正确决策的基础。新scan的flat分类丢失了这个关键设计，导致Manager无法区分"自己建工位"和"委派Worker"。
- alternatives_considered: (1)完全回退到旧scan — 丢失新scan改进；(2)在batch层面补丁 — 治标不治本。选择：融合两个版本的优点。
- boundary_non_goals: 不改prompt builder消费scan的逻辑；不改agent-table/agent-working；不改A2A task创建逻辑。
- residual_risk: station检测依赖issue.md的phase_state字段准确性——如果phase_state不准确，station检测也会偏差。
