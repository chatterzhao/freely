# Tasks: I-20261114T111702Z-A
- T1: RED 测试先行（AT-001 基线 8 ok / 2 failed）
- T2: 同行替换 cmd_comment 两处 ${PROJECT_ROOT} → ${SELF_ROOT}
- T3: 用封装命令 freely projections record 记录投影变更
- T4: GREEN（AT 10 ok / 0 failed；test-all 50 ok / 0 failed）
- T5: test 工位同步 dev 提交后重跑 test-gate
- T6: PR 门禁合并与 wt-close 收口
