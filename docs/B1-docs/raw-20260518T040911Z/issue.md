---
kind: raw
priority: P1
phase_state: absorbed
source: feedback
created_at: '2026-05-18T04:09:11Z'
title: auto_consume 调用处传入硬编码 raw_key，application 永远消费不到 worker handoff
platform_ids:
  github:
    issue_id: '553'
    url: https://github.com/chatterzhao/freely/issues/553
    synced_at: '2026-05-18T04:09:17Z'
updated_at: '2026-06-17T00:19:57Z'
primary_platform: github
platform_state: closed
local_id: raw-20260518T040911Z
---

## 根因

`auto_consume` 的 WHERE 设计是正确的（按 raw_key 分组消费）。问题在调用处：

```bash
# freely:13929 — manager 写 handoff 时的 raw_key
raw_key="manager-patrol"          # 硬编码！

# freely:14089 — 三处退出都读这个值
_rk_del="$(_db_exit_contract_field "$project" application raw_key)"
python3 "$_hp_del" auto-consume --raw-key "$_rk_del"
# → auto_consume("manager-patrol") → WHERE raw_key='manager-patrol' → 0 rows
```

而 worker 的 raw_key 是从 prompt 文件名正确提取的（freely:12084）：

```bash
_raw_key="$(echo "$_prompt_file" | grep -oE '[0-9]{8}T[0-9]{4,6}Z' | head -1)"
# → raw_key = "20260518T1005Z" ✅
```

**application 传 "application-patrol"，worker 用任务 key。永远不匹配。**

## 修复

不改 `auto_consume`，改三处调用方动态获取正确的 raw_key。

freely 14040/14077/14089 行（stop_ai / resume_application / delegate_workers）：

从 `worker_prompts_csv` 提取所有唯一步 raw_key，逐个调 `auto_consume`：

```bash
# 替代原来的单次 auto_consume("application-patrol")
local _worker_csv _prompt_file _rk
_worker_csv="$(_db_exit_contract_field "$project" application worker_prompts_csv)"
if [[ -n "$_worker_csv" ]]; then
  for _prompt_file in $(echo "$_worker_csv" | tr ',' ' '); do
    _rk=$(echo "$_prompt_file" | grep -oE '[0-9]{8}T[0-9]{4,6}Z' | head -1)
    [[ -n "$_rk" ]] && python3 "$_hp" auto-consume --db "$_db" --raw-key "$_rk" >/dev/null 2>&1 || true
  done
fi
```

这样 `consumed_by` 从 `'worker'` 更新为 `'application'`。

## 涉及文件

- `docs/system/workspace/scripts/runtime/freely` — 14040/14077/14089 三处 auto_consume 调用
- `docs/system/workspace/scripts/runtime/handoff.py` — 不改
