# Pre-Tests: worker handoff inject
- issue_id: I-20260511T0229Z-A
## Unit
- acceptance target: worker prompt 包含 handoff_id 和 db_path
^- status: passed
## Integration
- acceptance target: worker AI 能根据注入指令更新 handoff 状态
- testing layer: end_to_end
- target environment: evot project
- required evidence: worker 完成后 handoff 状态变为 completed
- status: pending_e2e
