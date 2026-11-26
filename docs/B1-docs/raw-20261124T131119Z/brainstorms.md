## 0. 设计意图审计（先于方案）

### 广搜与分层
- 关键词：close-local-id / stale linked / platform_ids / issue-sync close。命中 `platform-adapter.py:1304`、`raw_lifecycle_effects.py:99,219`、`cmd-close.sh`、`bin/issue-sync:100-150`。
- 当前生效实现：adapter 的 `close_local_id()` 已能按 local_id 枚举所有 OPEN 副本并汇总双平台结果；缺口仅在 packaged 入口。
- 历史文档：goal 中关于「手工 adapter 调用」的记录仅作反例，不是现状。

### 外部锚点
- `platform-adapter.py:1304`：`Close EVERY OPEN replica of local_id, mapped or not`。
- raw #4687 实证：手工 `import platform_adapter` 造成 `github: closed / gitee: error` 的部分成功伪装。
- `commands.md` 的意图→命令速查：平台写必须由封装命令经 adapter 完成。

### 判定
**实现未完成**：底层能力现成，缺一个 packaged 命令与可操作回执。

### 冲突 / 影响面
无既有断言冲突；影响 `bin/issue-sync` 动作表、`cmd-close.sh`、`commands.md` 与 AT。

## 0.1 全局适配四问
- Q1：流程能力（封装入口）。
- Q2：与 `issue-sync batch`/`wt-close` 共享平台写职责；adapter 仍是唯一写者。
- Q3：不要求额外工位或 IBM 流程，命令是一次性平台治理动作。
- Q4：门禁测文件/身份，本轮补的是命令可达性；不改门禁。

## 1. 决策
新增 `issue-sync close-orphans <local_id> [linked|raw]`：读取本地 doc 的 platform_ids 作为提示，委托 adapter `close-local-id` 枚举真实副本；逐平台结果原样打印，rc 0/3/1 透传，失败打印可复制重试命令。不写本地 frontmatter（平台治理动作，非生命周期推进）。
