# PRD: 全项目旧路径引用清理

## 目标

清除 `docs-structure-refactor` PR 遗漏的旧路径引用，使 19 个核心脚本正确读写新目录结构。

## 路径映射

| 旧路径 | 新路径 | 策略 |
|--------|--------|------|
| `docs/issues/raw-{key}/issue.md` | `docs/B1-docs/raw-{key}/issue.md` | sed |
| `docs/issues/I-{key}/issue.md` | `find docs/B2-docs -path "*/issues/I-{key}*.md"` | find 搜索 |
| `docs/epics/` | `docs/B2-docs/` | sed |
| `docs/progress/` | `docs/B2-docs/` | sed |
| `.freely/intake/` | `docs/B1-docs/` | sed |

## B2-docs I-* 查找策略

两阶段搜索：
1. Pattern A: `find docs/B2-docs -path "*/raw-{raw_key}*/issues/I-{key}*.md"`（通过 raw_key 定位）
2. Pattern B fallback: `find docs/B2-docs -path "*/issues/I-{key}*.md"`（老格式无 raw- 目录）

## 实施阶段

1. 批量 sed：`docs/epics`→`docs/B2-docs`（所有文件安全）
2. 批量 sed：`docs/issues`→`docs/B1-docs`（仅纯 raw-* 引用文件）
3. 手动修复：I-* 引用改用 B2-docs find 搜索
4. 扩展清理：docs/progress/, .freely/intake/
5. 验证：bash -n 检查，git diff 审查，端到端路径验证
