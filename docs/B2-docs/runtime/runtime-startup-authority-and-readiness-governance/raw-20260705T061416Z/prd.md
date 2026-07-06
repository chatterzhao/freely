# PRD: fix dirty 提示 backtick 命令替换

- issue_id: I-20260705T061416Z-A

## Goal

修复 `freely daemon start` 执行 dirty check 时，提示文本中的反引号被 bash 当作命令替换导致 `command not found` 错误。

## 实现方案

单行修改 `docs/system/workspace/scripts/runtime/freely:21982`：

```diff
-      log_error "    详细流程见 skill \\`freely-workflow-guarded-execution\\`"
+      log_error "    详细流程见 skill freely-workflow-guarded-execution"
```

### 为什么这么改

- `log_error()` 使用 `echo "$*"`，参数在双引号内展开
- `\\` 在双引号中被转义为字面 `\`，随后裸反引号触发命令替换
- 去掉反引号是最简单、最安全的方案
- 纯文本输出 skill 名称，语义不变

## 影响面

| 文件 | 改动 |
|------|------|
| `docs/system/workspace/scripts/runtime/freely` | 1 行：去掉反引号转义 |

## Dev-Loop Handoff

- 修改 1 行 → 保存 → 验证 `bash -n` 语法 → 测试 dirty 检查场景不再报 command not found
