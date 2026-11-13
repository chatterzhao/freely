# Tasks — raw-20261113T115957Z

- [x] T1: 定位三处实现缺陷（B1 路径 / 只读 absorbed_into / 无终态检查）
- [x] T2: wt-close 新增 Phase 2.5（promoted_children + B2 路径 + 终态门禁 + 逐个关闭 + dry-run/skip-platform）
- [x] T3: 新增 AT test-wt-close-children.py，CORE/CI_CORE 各 +1；RED 4/14 → GREEN 15/0
- [x] T4: PR → review → merge → 用新 wt-close 收口本轮 child → wt-close
