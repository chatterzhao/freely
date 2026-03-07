---
name: config-backup-guard
description: 强制配置修改前的必要备份。当 AI 修改任何配置文件时使用，在编辑前创建可追溯的备份和恢复路径。
---

# skill:config-backup-guard

## 工作流
1. 在编辑前检测目标配置文件。
2. 使用统一命名创建备份：`<original-basename>.bak.<YYYYMMDD-HHMMSS>`（UTC）。
3. 在记录中保留源文件路径、备份文件路径和预期恢复目标。
4. 仅在备份成功后应用变更。
5. 在执行笔记中记录备份路径和时间戳。

## 完成
- 每个配置变更都有可恢复、可追溯且命名一致的备份产物。
