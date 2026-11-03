# PRD：report/attention + prompt manifest（I-C）

## Goal

把交接从“自由文本 summary”升级为可查询的 report/attention；把 prompt 缓存从“注释里的顺序”升级为可记录、可比较的 manifest。

## 1. report

```json
{
  "task_id": "T-1",
  "role": "worker",
  "report_state": "ready",
  "summary": "done",
  "next_action": "review",
  "attention": {
    "needed": true,
    "question": "是否接受这个边界？",
    "target_role": "manager",
    "target_session": null,
    "human_action": "确认",
    "for_trigger_id": "event-1"
  }
}
```

六态：progress/waiting/ready/blocked/failed/dropped。attention.needed=true 时只能一个问题，target_role 必填；false 时其余字段为空。

## 2. 批量决策

```json
{"decisions":[
 {"trigger_id":"e1","decision":"accept","reason":"explicit"},
 {"trigger_id":"e2","decision":"ignore","reason":"duplicate"}
]}
```

decision ∈ accept/stop/ignore/unavailable；每条 reason 必填；trigger_id 幂等。

## 3. 存储

- `agent_reports(report_id PK, task_id, role, report_state, summary, next_action, attention_json, created_at)`
- `agent_decisions(decision_id PK, trigger_id UNIQUE, decision, reason, created_at)`
- 同一 DB `freely.db`；A2A/Manager 可查。

## 4. CLI

```
a2a-report record --project . --task-id T --role worker --report-state ready --summary ... [--attention-json ...]
a2a-report list --project . [--task-id T]
a2a-decide record --project . --decisions-json '[...]'
a2a-decide list --project .
```

## 5. prompt manifest

- 标记：`<!-- FREELY_SEGMENT:name -->`。
- `split_prompt` 返回段名/内容；无标记返回 `full_prompt`。
- `build_manifest` 输出 segments/prefix_hash/usage_source/cache_source。
- prefix = 前 4 个 stable/semi 段；tail 变化不影响 prefix hash。
- `run-acp-prompt.py` 每次 prompt 写 `.freely/run/prompt-manifest.jsonl`。
- 只记录，不改变 prompt 内容。

## 6. 非目标

- 不改 Manager 批量路由决策逻辑。
- 不做完整 11 段 prompt 重构；没有 marker 就如实记 full_prompt。
- 不做真实 patrol 对照；test 阶段用两个 prompt fixture 对照。

## 7. 验收

- report 六态/attention 校验；非法拒绝。
- 批量决策幂等/逐条 reason。
- manifest 段解析/prefix 稳定/reported 才算 hit rate。
- CLI record/list 可用；run-acp-prompt 日志存在。
