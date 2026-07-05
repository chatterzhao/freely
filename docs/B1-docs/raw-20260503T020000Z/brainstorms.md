# Brainstorm: Scan Lifecycle Migration

## 问题
task-source-scan.py 已废弃但仍在使用，输出147条噪声。新版 task-lifecycle-scan.py 已写好但从未接入 runtime。

## 决策
- 切换到 task-lifecycle-scan v2
- 以 raw→I 链条追踪替代5个平铺 surface
- 增加 Phase 0 信号扫描（chat inbox）
- 分支命名规范强制（gate 兜底）
- AF_UNIX socket 路径用 hash 缩短

## 收敛
已完成实现和 test-pre-merge 验证，scan 输出从147条降到35条精准结果。
