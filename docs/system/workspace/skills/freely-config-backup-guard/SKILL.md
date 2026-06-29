---
name: freely-config-backup-guard
description: >- 强制配置修改前创建可追溯备份。在编辑任何配置文件之前自动创建
  备份和恢复路径，防止误改无法回滚。

  Use when: AI 修改任何配置文件（config.toml、settings.json 等）。
  触发词："改配置"、"备份配置"、"config backup"、"修改 settings"。
---

# skill:freely-config-backup-guard

## 工作流

1. 先读取 [applicability-and-recovery.md](references/applicability-and-recovery.md) 判断目标是否属于需要备份的配置文件。
2. 在编辑前检测目标配置文件。
3. 使用统一命名创建备份：`<original-basename>.bak.<YYYYMMDDTHHMMSSZ>`（UTC）。
4. 在记录中保留源文件路径、备份文件路径和预期恢复目标。
5. 仅在备份成功后应用变更。
6. 在执行笔记中记录备份路径和时间戳。

## 完成
- 每个配置变更都有可恢复、可追溯且命名一致的备份产物。
