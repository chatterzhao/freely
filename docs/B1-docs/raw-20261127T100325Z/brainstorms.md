## 0. 设计意图审计
### 外部锚点
- #4731 现场：issue-sync create PARTIAL 后 shell 抛 `raw_key： unbound variable`，真实失败回执被掩盖。
- `set -u` 下 shell 标识符边界：`$var：` 会把全角标点纳入变量名。
### 判定
**实现偏差（shell 引号边界）**，不是设计问题；不改 fail-closed 策略。
### 冲突 / 影响面
只改失败回执变量引用与 AT；不改平台写、不改判据。
## 0.1 四问
Q1 治理提示语 bug；Q2 与 issue-sync 的部分成功汇总共享职责但不改其语义；Q3 不要求额外工位；Q4 AT 直接断言 stderr 文本。
## 1. 决策
用 `${raw_key}` 显式边界；新增全角标点邻接扫描 + stub 行为 AT。
