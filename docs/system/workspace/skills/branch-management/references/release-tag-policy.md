# 发布和标签策略

## 阶段格式
- 标签格式必须为：`YYYY.MM.DD-HHMM-stage`
- `stage` 是必需的，不可省略。

## 按分支的阶段
- `feature/*` -> `alpha`（本地轻量标签，不推送）
- `pre-test-merge` -> `beta`（本地轻量标签，不推送）
- `develop` -> `nightly`（推送标签）
- `main` -> `stable`（推送标签）
- `hotfix/*` -> `hotfix`（推送标签）

## 发布分支流程
1. 从 `develop` 创建 `release/*`。
2. 冻结并验证发布内容。
3. 将 `release/*` 合并到 `main`。
4. 将发布结果回合并到 `develop`。

## 热修复流程
1. 从 `main` 创建 `hotfix/*`。
2. 将热修复合并到 `main` 和 `develop`。
3. 若 `pre-test-merge` 当前活跃，将热修复结果同步到 `pre-test-merge`。

## 保护措施
- 绝不推送 `alpha`/`beta`。
- 如必需测试或治理检查失败，阻止发布并阻止推送标签。
