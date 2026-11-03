# Tasks: I-20261103T091157Z-A

| ID | 任务 | 产物 | 依赖 | 验收 |
|---|---|---|---|---|
| T1 [x] | Gitee search 分页 RED 测试 | test-platform-adapter-gitee-search.py | — | AT-001 |
| T2 [x] | 实现 Gitee search 分页 | platform-adapter.py | T1 | AT-001 |
| T3 [x] | parity 测试（open 集合相等；本地文档校验可选） | test-platform-open-parity.py | — | AT-002 |
| T4 [x] | 关闭 4 个 Gitee 漂移镜像 | gitee issues | T2 | AT-003 |
| T5 [ ] | follow-up docs-only lane：物化 13 个 open raw 文档 + 回填 13 个历史编号 | docs/B1-docs/raw-*/issue.md | merged | AT-002 --require-local-docs |
