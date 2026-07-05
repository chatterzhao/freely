# Brainstorm — raw key 格式统一

## 现状

```
来源                         格式                      示例
──────────────────────────────────────────────────────────────────
GitHub issue title           RAW-YYYYMMDDTHHMMZ        RAW-20260504T1145Z
本地 docs/B1-docs/ 目录        raw-YYYYMMDD-HHMM          raw-20260503-0200
chat-inbox freely.db         YYYYMMDDHHMMSS (14位)      20260503105742
pre-brainstorm 目录           {key}--{slug}              20260503-0200--scan-lifecycle
feature 分支                  feature/raw-{key}-{slug}   feature/raw-20260503-0200-foo
```

## 为什么有问题

1. `pre-push.sh` regex `raw-[0-9]{8}-[0-9]{4}` 只认本地格式，GitHub 格式分支 push 被拒
2. `wt-create _extract_issue_key` 同样只认 `[0-9]{8}-[0-9]{4}`
3. `task-lifecycle-scan.py` I-* 后缀解析、B1 目录 glob、分支 key 提取都只认连字符格式
4. `governance-merge-gate` GATE 2a 自动 materialize 只匹配 `(\d{8}-\d{4})`
5. chat-inbox DB 14 位秒精度与分钟精度不匹配——wt-create 用分钟精度 key 查 DB 秒精度 ID

## 目标格式

**`YYYYMMDDTHHMMZ`**（ISO 8601 紧凑型，分钟精度，UTC）

理由：
- GitHub issue-sync 已经使用此格式（`[RAW-20260504T1145Z]`）
- ISO 8601 标准，无歧义
- `T` 和 `Z` 天然分隔，不依赖连字符位置
- 分钟精度足够区分同一分钟内的 issue（通过后缀 A/B/C）

## 过渡策略

- **历史不动**：已有 raw-YYYYMMDD-HHMM 目录/分支保持不变
- **新物用新格式**：新创建的 raw issue、pre-brainstorm 目录、feature 分支用新格式
- **代码双兼容**：所有 regex/glob 同时接受新旧格式
- **chat-inbox DB id 不变**：chat_id 继续用 14 位秒精度（SQLite 内部实现细节，不与外部 key 耦合）

## 不做的事

- 不迁移历史 raw/I-*/pre-brainstorm 目录
- 不改已有的 feature 分支名
- 不改 chat-inbox.py 的 `_utc_timestamp()`（DB 内部格式）
- 不强制重命名已有的 GitHub issue

## 受影响文件

关键路径（必须改）：
1. `pre-push.sh` — 分支命名 gate：regex 加新格式
2. `wt-create` — `_extract_issue_key`：同时匹配新旧
3. `task-lifecycle-scan.py` — `_extract_issue_key_from_branch`、`_base_key`、I-* 解析、B1 目录 glob
4. `governance-merge-gate` — GATE 2a regex
5. `freely` — `_route_chat_to_issue` 消息路由 regex

文档更新：
6. `ibm-framework.md` — ID 格式说明
7. `docs/LAWS.md` — 如有引用
8. skill 文档中的示例 — 更新为新格式示例

## 备选方案

**方案 B：统一为 YYYYMMDD-HHMM（本地格式）**
- 需要改 issue-sync 的 `_platform_title`，GitHub issue 标题格式随之改变
- 改动面更大（涉及平台→本地→平台双向）
- 否决：ISO 格式是国际标准，平台侧用 ISO 更合理

**方案 C：统一为 Unix 秒时间戳**
- 人类不可读
- 否决：raw key 出现在目录名、分支名中，必须可读
