# PRD: worker 派发 JSON 化 + 边界 lint
- issue_id: I-20261109T085539Z-A
- source_raw: raw-20261109T085539Z
- milestone: M-20261109T085539Z-A

## 问题
TSV 传 AI prompt，含 tab 即错位；`except: pass` 吞畸形输入；`python3 -c` 插值缺机械边界。

## 目标
1. 派发走 JSON Lines，NUL 分隔流交给 bash，AI 文本永不进 shell 语法。
2. 畸形行显式报告 + 计数，不再表现为「无任务」。
3. lint 提供可计数基线与「禁止新增」边界。
4. 保持派发循环体与其它 3 处 TSV 通道不变。

## 非目标
状态文件协议迁移（拆 #4252）、一次性替换 108 个 lint 候选、平台 failover。

## 验收
见 verification/pre-tests.md 的 AT-001。
