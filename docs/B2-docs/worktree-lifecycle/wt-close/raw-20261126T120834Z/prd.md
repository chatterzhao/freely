# PRD: raw-20261126T120834Z

## Goal
让 wt-close 的退役门禁与 #4703 的三态测试证据判定一致：元数据等价提交可沿袭，真代码变更必须重跑。

## 实现
仅修改 `docs/system/workspace/scripts/quality/pretests-retirement-gate`：
- 删除 `_latest_commit`/`_last_tested_commit` 精确相等比较及其 `pretests_stale` 报错分支；
- 保留其后的 `test-evidence.py validate --json` 调用与 `ok` 判定，并在诊断里输出三态 verdict。

## 非目标
不改 `test-evidence.py`、不改 `wt-close`、不改 CI 证据链其他消费者。

## Dev-Loop Handoff
RED：AT 结构断言在 develop 命中自造判据，行为断言中 equivalent 场景 rc=1；GREEN：三态全绿 + 既有 test-evidence 单测回归。
