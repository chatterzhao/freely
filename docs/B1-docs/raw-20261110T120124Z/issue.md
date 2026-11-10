---
schema_version: '1'
local_id: raw-20261110T120124Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261110T120124Z-A
platform_ids:
  github:
    issue_id: '4281'
    url: https://github.com/chatterzhao/freely/issues/4281
    synced_at: ''
  gitee:
    issue_id: IKUEMX
    url: https://gitee.com/zhaoquan/freely/issues/IKUEMX
    synced_at: ''
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/daemon/raw-20261110T120124Z/issues/I-20261110T120124Z-A.md
last_synced_comment_at:
  github: '2026-11-10T12:17:01Z'
  gitee: '2026-11-10T12:17:01Z'
hash: ''
created_at: '2026-11-10T12:01:24Z'
updated_at: '2026-11-10T12:26:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children:
- I-20261110T120124Z-A
source_candidate: ''
completed_at: '2026-11-10T12:17:00Z'
closeout_note: ''
severity: P2
---

# fix: #4157 剩余可观测性与运维底座分项

workflow_kind: fix

从 #4157（raw-20261103T132644Z）拆分。原 issue 8 个分项，R25 已完成分项 1（will now stop 分支 exit 1）与分项 6a（bin/freely 的 Python >= 3.11 前置）；分项 5 的 --output / 与 --output ~ 守卫已由 #4158 落地。本 issue 承接剩余 6 项。

## 根因

失败被表达成正常或降级告警、跨进程无关联 id、日志与打包路径无界、凭据进入 argv/URL、DB 迁移失败被吞。

## 影响

单项都不算 P0，但共同构成「出问题后无人知道」的运维底座：watchdog 死亡无人发现、排障只能靠人拼文件、安装包带出缓存与死代码、同机可见明文密钥。

## 修复方案

1. bin/freely-watchdog：tail -f 目标不存在时 pipefail 静默非零退出；PRE_CHECK_MAP 的 return 1 在 set -e 下结束 while 子壳，第一次违规后 watchdog 死亡；:10 是第四套 worktree 根推导。加 pid + 轻量守护，或明确降级为人工诊断工具；return 1 改 continue + 计数。
2. append_runtime_event（freely:1436-1452）缺 severity / trace_id，120 个调用点只有 32 处带 raw_key，%q 转义难机器解析。增加 severity 与 trace_id，补 raw_key，保持 lifecycle-trace 有序。
3. 日志无界：仅 5 个固定名日志有轮转；cycle-.log、cycle-worker-.log:13311、crash-*.log:23685 无轮转（实测 .freely/logs 71 文件 / 4.1MB）。接入 _rotate_log 并设保留数。
4. 打包卫生：bin/freely-package 的 cp -R 会把 __pycache__/ 与 *.bak.py（如 task-lifecycle-scan.bak.py，2,007 行）装进安装态。复制后排除并重新计数。
5. 凭据暴露面（P1）：ai-cli:927 把 api_key 放 argv（同机 ps 可见）；ai-cli:2392 支持 --key 进 shell history；gitee-issue.py:120-127 把 access_token 放 URL query。argv 改 stdin/env；query 改 Authorization 头。
6. 环境与文档：DB 无 schema_version / PRAGMA user_version，迁移包在 except: pass（freely_db_manager.py:276-297）；.env.example 指向 config.toml + toml2env；skills/README.md 补 7 个执行面 skill 的角色归属。

## 验收标准

- RED：构造 PRE_CHECK_MAP 违规 / 缺 tail 目标 → watchdog 不再静默死亡；--output 保留 #4158 现有守卫。
- GREEN：append_runtime_event 输出含 severity= 与 trace_id=，awk 可稳定解析；.freely/logs 下 cycle-*/crash-* 有保留上限；打包产物无 __pycache__ 与 *.bak.py；ps -ef 与 shell history 无明文 api_key；token 不出现在 URL；DB 有 user_version 且迁移失败不吞。
- 不退化：不改 lifecycle-trace 的 seq 语义、不改 #4157 已完成的 exit 1 / Python 前置、不改 #4158 的 output 守卫。

### comment-20261110T121700Z
- source: system
- event: promote_finalized
- children: ["I-20261110T120124Z-A"]

拆解为以下任务:
1. [I-20261110T120124Z-A](will-be-updated)
