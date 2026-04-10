# Brainstorm - 20260410-1430--preferred-auth-method-account-switch-fix

## Problem

在 `I-20260405-0027-A` 实现的 Codex slot bundle 逻辑中存在一个 bug：当从 apikey slot 切换到 account slot 时，`preferred_auth_method` 字段从 live config 中被删除后无法恢复，因为 account slot 的 `config-auth.toml` fragment 是空文件。

## Confirmed Facts

- `codex_apply_saved_slot_config_fragment` 函数在 L793 执行 `data.pop("preferred_auth_method", None)` 先删除该字段
- L802 尝试从 fragment 恢复，但 account slot 的 fragment 是空的
- 结果：`preferred_auth_method` 字段永久丢失
- 测试 `test-ai-cli-codex-apikey-slot-bundle-switch` 未覆盖此场景

## Root Cause Analysis

```
codex_save_live_bundle_to_slot():
  if kind == "apikey":
    codex_write_fragment_toml_from_live_config(...)  # 保存 config 片段
  else:
    : >"$config_fragment"  # account 类型创建空文件！
```

切换时：
1. 先删除 live config 中的 `preferred_auth_method`
2. 从 fragment 恢复
3. account fragment 为空 → 无法恢复

## Boundary

这是 `I-20260405-0027-A` 的 narrow bug fix，不重新打开：
- slot bundle 架构设计
- 跨工具 slot 契约
- standalone `ai-switch-cli` 提取时机

## Proposed Fix

在 `codex_apply_saved_slot_config_fragment` 中添加 fallback 逻辑：当 fragment 没有设置 `preferred_auth_method` 时，根据 `slot_kind` 设置默认值：
- `account` → `"chatgpt"`
- `apikey` → `"apikey"`

## Open Questions

无。这是边界清晰的 bug fix。

## Acceptance Criteria

1. 切换到 account slot 后，`preferred_auth_method = "chatgpt"` 在 live config 中存在
2. 切换到 apikey slot 后，`preferred_auth_method = "apikey"` 在 live config 中存在
3. 现有测试继续通过
4. 新增测试断言覆盖 account 切换场景
