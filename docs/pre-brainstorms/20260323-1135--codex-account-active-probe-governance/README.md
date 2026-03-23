# Codex 账号主动探测治理

## 状态
🟡 CONVERGING

## 背景
当前账号可用性检查是被动模式：
1. 仅检查本地 `codex-account-cooldowns.tsv` 文件
2. 只有在 rate limit 耗尽时才记录 cooldown
3. cooldown 记录可能过时（账号提前恢复不会自动更新）

## 问题
1. **被动依赖记录**: `codex_account_is_available_now()` 只检查本地文件，不实际探测
2. **探测时机有限**: 仅在 `ensure_codex_account_ready_for_manager()` 的第三步才主动探测
3. **无定期健康检查**: 没有定期对所有账号进行可用性探测
4. **性能问题**: 用户反馈 `watch` 模式消耗性能

## 目标
在合适时机主动探测所有账号状态：
1. 探测所有账号，更新 cooldown 账本
2. 切换到可用账号
3. 如果都不可用，切换到最早可恢复的账号

## 现有关键实现

### 文件位置
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
  - `codex_probe_current_account_now()` - 探测当前账号
  - `probe_any_usable_codex_account_now()` - 遍历探测所有账号
  - `switch_to_codex_account()` - 切换账号
  - `select_earliest_reset_codex_account()` - 选择最早恢复的账号

### 现有探测逻辑
```bash
# 探测当前账号（实际调用 codex exec）
codex_probe_current_account_now() {
  # 构造简单 prompt: "Reply with exactly: OK"
  # 执行 codex exec，检查返回
}

# 遍历所有保存账号，找到可用的
probe_any_usable_codex_account_now() {
  while IFS= read -r candidate; do
    switch_to_codex_account "$project" "$candidate"
    if codex_probe_current_account_now "$project"; then
      codex_clear_account_cooldown "$project" "$candidate"
      printf '%s\n' "$candidate"
      return 0
    fi
  done < <(codex_saved_accounts "$project")
}
```

## 改进方案

### 1. 新增命令: `freely ai probe-all`
主动探测所有保存账号，更新 cooldown 账本。

```bash
# 用法
freely ai probe-all codex [--project /path]

# 输出
# - 成功: 打印可用账号名
# - 失败: 打印最早恢复的账号和时间
```

### 2. 触发时机
不使用 watch，在以下时机执行：

| 时机 | 触发点 |
|------|--------|
| Manager 启动前 | `ensure_manager_once()` 开头 |
| Rate limit 耗尽后 | `cmd_start()` 检测到 rate limit |
| 用户手动触发 | `freely ai probe-all` |

### 3. 探测流程
```
probe_all_codex_accounts()
    |
    +-- 遍历所有保存账号
    |       |
    |       +-- 切换账号
    |       +-- 执行 codex exec "hi" (带代理)
    |       +-- 超时 15 秒
    |       |
    |       +-- 成功: 清除 cooldown，记录为可用
    |       +-- 失败: 解析 "try again at" 时间，记录 cooldown
    |
    +-- 返回结果:
            - 有可用账号: 切换并返回账号名
            - 全部冷却: 切换到最早恢复的账号
```

### 4. 冷却时间解析
从错误消息中解析 "try again at Mar 23rd, 2026 3:51 PM" 格式：

```bash
parse_try_again_time() {
  local output="$1"
  # 提取 "try again at ..." 并转换为 Unix 时间戳
  # 格式: Mar 23rd, 2026 3:51 PM
}
```

## 实现计划

1. [ ] 增强 `probe_any_usable_codex_account_now()`
   - 解析 rate limit 错误消息
   - 记录 cooldown 时间戳

2. [ ] 新增 `probe_all_codex_accounts_and_update_cooldown()`
   - 遍历所有账号，探测并更新账本
   - 返回可用账号或最早恢复的账号

3. [ ] 修改 `ensure_codex_account_ready_for_manager()`
   - 在开头调用主动探测
   - 使用探测结果更新决策

4. [ ] 新增 `cmd_probe_all()` CLI 命令
   - 支持手动触发探测

## 约束
- 探测需要带代理: `ALL_PROXY="http://127.0.0.1:7890"`
- 超时时间: 15 秒/账号
- TSV 文件格式保持兼容: 增加 human-readable 列

## 相关文档
- `docs/pre-brainstorms/20260318-1630--global-ai-account-watchdog/`
- `docs/pre-brainstorms/20260317-0735--account-aware-loop-and-checkpoint-commit-governance/`
