## 0. 设计意图审计
### B0 前置广搜
- 关键词族：`FREELY_SKIP_IBM_GATE` / `is_governance_only_path` → `governance-merge-gate:359-440,1115`；`GATE 1: timestamp mismatch` → `:1286-1298`；`batch scope` → `cmd-batch.sh:5-30`、`.freely/config.toml:59-60`。
- 三类分层：当前生效 = config 优先 + batch `scope=` 过滤；历史局部 = gate 硬编码 L2 默认与 GATE 1 旧诊断；权威 = raw-20261103T091157Z 的 governance-only lane 设计。
- 矛盾清单：代码注释说 config 是唯一真源，但 L2 硬编码仍存在；GATE 1 报错不给放行命令；batch 有 scope 但无显式 `--raw-key`。
- 二元决策：继续——接线三条缺口，不放宽 implementation 路径。
### 外部锚点
- `docs/LAWS.md` 一个工位一个 issue；raw-20261103T091157Z 的 lane 设计原文；`config.toml [skip_ibm_gate].allowed_paths`。
- 判定：实现偏差（设计已存在、接线未完成）。
- 影响面：gate 白名单解析、GATE 1 诊断文本、issue-sync batch 参数与提示、AT。
## 0.1 四问
Q1 流程能力；Q2 config 拥有白名单真源，gate 只消费；Q3 不新增第三种 lane；Q4 AT 断言两种 lane 的边界与白名单差集为空。
## 1. 决策
config 单源；GATE 1 追加 lane 指引；batch 支持 `--raw-key` 且全量打印治理 lane 提示。
