---
local_id: raw-20260521T095313Z13Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '1770'
    url: https://github.com/chatterzhao/freely/issues/1770
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T09:53:25Z'
updated_at: '2026-06-17T00:21:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-05-21T15:26:25Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
platform_state: closed
---

## 问题

当前 Freely 对 AI_TOOL=cc-ai98pro-0045-auto 这类 shell alias 的解析存在三个断裂点：

### 1. 硬编码前缀匹配（临时方案，不通用）
_resolve_tool_family 里加了 cc-* 硬编码前缀。每新增一种 alias 命名风格就要加新规则。

### 2. alias 命令只能解析别名
_apply_tool_alias_settings 和 _resolve_tool_family 用 ${SHELL} -ic "alias" 来解析。这只对 alias 有效，对 shell function 或 wrapper script 无效。

### 3. CLAUDE_CODE_SETTINGS_FILE 从未被导出（Python bug）
_apply_tool_alias_settings 里 Python f-string {alias_path} 被当作 Python 变量求值导致 NameError，被 except:pass 静默吞掉。

## 设计

用 ${SHELL} -ic "type <tool>" 替代 ${SHELL} -ic "alias <tool>" 作为统一解析入口。

type 输出格式（zsh/bash 通用）：
- 别名: name is an alias for binary --settings /path --flags
- 二进制: name is /path/to/binary
- 函数: name is a shell function from ...

统一解析函数 _resolve_tool_full <name> 输出 family|binary|settings_path

逻辑：
1. ${SHELL} -ic "type name" 获取类型和展开
2. 如果包含 "is an alias for" → 提取 expansion → 解析 binary + --settings path
3. 如果包含 "is /"（二进制路径）→ 提取 basename → 映射到 family
4. binary → family 映射: claude→cc, codex→codex, kiro-cli→kiro-cli, iflow→iflow, opencode→opencode

## 效果

- 任何新 alias 无需改代码
- 同时支持 alias / function / 二进制三种形式
- type 输出更规整，解析更可靠
- 不再需要 cc-* 硬编码前缀
- Python f-string bug 一并修复
