# runtime/freely 拆分计划（cmd_* 依赖矩阵）

- 单体：`docs/system/workspace/scripts/runtime/freely`（27158 行，935 个函数，56 个 `cmd_*` 入口）
- 生成方式：解析单体顶层函数定义，逐个 `cmd_*` 提取「体量 / 单体内部依赖 / state 键 / 平台调用 / 已外移的 bin」，不是手工估的
- 已外移（`exec bash "$SELF_ROOT/bin/<cmd>"`）：**15** 个
- 分阶段：phase 0 (done) = 15，phase 1 (next) = 6，phase 2 = 22，phase 3 (last) = 13

## 阶段定义

| phase | 含义 | 判据 |
|---|---|---|
| 0 | 已外移 | 函数体只有 `exec` 投影 |
| 1 | 可立即外移 | 内部依赖 ≤3 且 state 键 ≤3：抽走后只需 `lib/common.sh` |
| 2 | 需先抽 helper | 内部依赖 4–8：先把共用 helper 挪进 `runtime/lib/` |
| 3 | 最后做 | 内部依赖 >8 或触碰 daemon/dispatch 状态机 |

## 依赖矩阵

| # | phase | cmd | 行 | 行数 | 内部依赖 | state 键 | 平台 | bin 下游 |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 (done) | `cmd_checkpoint_guard` | 27048 | 4 | — | — | — | `bin/checkpoint-guard` |
| 2 | 0 (done) | `cmd_cycle` | 27032 | 4 | — | — | — | `bin/freely-cycle` |
| 3 | 0 (done) | `cmd_deploy_skills` | 27040 | 4 | — | — | — | `bin/deploy-skills` |
| 4 | 0 (done) | `cmd_evidence_add` | 8778 | 4 | — | — | — | `bin/evidence` |
| 5 | 0 (done) | `cmd_governance_check` | 27044 | 4 | — | — | — | `bin/governance-check` |
| 6 | 0 (done) | `cmd_pr_create_guarded` | 27016 | 4 | — | — | — | `bin/pr-create-guarded` |
| 7 | 0 (done) | `cmd_pr_merge_guarded` | 27020 | 4 | — | — | — | `bin/pr-merge-guarded` |
| 8 | 0 (done) | `cmd_pr_review_guarded` | 27028 | 4 | — | — | — | `bin/pr-review-guarded` |
| 9 | 0 (done) | `cmd_pretests_gate` | 27052 | 4 | — | — | — | `bin/pretests-gate` |
| 10 | 0 (done) | `cmd_pretests_retirement_gate` | 27056 | 4 | — | — | — | `bin/pretests-retirement-gate` |
| 11 | 0 (done) | `cmd_test_gate_record` | 8782 | 4 | — | — | — | `bin/test-gate` |
| 12 | 0 (done) | `cmd_watchdog` | 27036 | 4 | — | — | — | `bin/freely-watchdog` |
| 13 | 0 (done) | `cmd_wt_close` | 27024 | 4 | — | — | — | `bin/wt-close` |
| 14 | 0 (done) | `cmd_wt_create` | 27012 | 4 | — | — | — | `bin/wt-create` |
| 15 | 0 (done) | `cmd_test_gate_run` | 8772 | 6 | `cmd_evidence_add` | — | — | `bin/test-gate` |
| 16 | 1 (next) | `cmd_issue_sync` | 26588 | 9 | — | — | issue-sync | `bin/issue-sync` |
| 17 | 1 (next) | `cmd_raw_issue_pull` | 26597 | 9 | — | — | — | `bin/raw-issue-pull` |
| 18 | 1 (next) | `cmd_feedback` | 25121 | 438 | — | — | adapter, issue-sync | — |
| 19 | 1 (next) | `cmd_auth_change_wake` | 24702 | 15 | `usage`, `wake_registered_projects_for_auth_change` | reason | — | — |
| 20 | 1 (next) | `cmd_comment` | 25028 | 93 | `abs_path_or_fail`, `resolve_project_or_fail` | PROJECT_ROOT | adapter | — |
| 21 | 1 (next) | `cmd_discuss` | 24929 | 99 | `abs_path_or_fail`, `resolve_project_or_fail` | PROJECT_ROOT | adapter | — |
| 22 | 2 | `cmd_daemon_run` | 24505 | 13 | `abs_path_or_fail`, `resolve_project_or_fail`, `start_project_runtime`, `usage` | — | — | — |
| 23 | 2 | `cmd_daemon_status` | 24463 | 13 | `abs_path_or_fail`, `cmd_live_status`, `resolve_project_or_fail`, `usage` | — | — | — |
| 24 | 2 | `cmd_daemon_stop` | 24449 | 14 | `abs_path_or_fail`, `resolve_project_or_fail`, `stop_project_runtime`, `usage` | — | — | — |
| 25 | 2 | `cmd_stop` | 26997 | 15 | `abs_path_or_fail`, `resolve_project_or_fail`, `stop_project_runtime`, `usage` | — | — | — |
| 26 | 2 | `cmd_sync_tooling` | 21673 | 15 | `abs_path_or_fail`, `resolve_project_or_fail`, `sync_project_tooling_from_source`, `usage` | — | — | — |
| 27 | 2 | `cmd_ensure_manager_watch` | 20845 | 30 | `ensure_manager_once`, `ensure_manager_watchdog_pid_file`, `stop_marker_file`, `valid_ensure_manager_watchdog_pid_for_project` | — | — | — |
| 28 | 2 | `cmd_chat` | 24846 | 61 | `abs_path_or_fail`, `resolve_project_or_fail`, `submit_human_frontdoor_message`, `usage` | — | — | — |
| 29 | 2 | `cmd_security_review_brief` | 24832 | 14 | `abs_path_or_fail`, `load_config`, `load_session_state_or_defaults`, `resolve_project_or_fail`, `usage` | — | — | — |
| 30 | 2 | `cmd_ensure_sse_watchdog_watch` | 20821 | 24 | `launch_sse_watchdog`, `sse_watchdog_claim_pid`, `sse_watchdog_pid_file`, `stop_marker_file`, `valid_sse_watchdog_pid_for_project` | — | — | — |
| 31 | 2 | `cmd_new_session` | 24205 | 25 | `abs_path_or_fail`, `exit_contract_file`, `resolve_project_or_fail`, `select_launch_kind`, `session_state_file` | FORCE_FRESH | — | — |
| 32 | 2 | `cmd_ensure_interruption_dispatch_watch` | 20774 | 27 | `ensure_interruption_dispatch_once`, `intake_pending_signal_file`, `interruption_dispatcher_pid_file`, `stop_marker_file`, `valid_interruption_dispatcher_pid_for_project` | — | — | — |
| 33 | 2 | `cmd_status` | 26606 | 67 | `abs_path_or_fail`, `cmd_baseline_status`, `cmd_fleet_status`, `cmd_live_status`, `usage` | — | — | — |
| 34 | 2 | `cmd_ensure_sse_watchdog` | 24741 | 24 | `abs_path_or_fail`, `check_doc_gate_or_fail`, `cmd_ensure_sse_watchdog_watch`, `load_config`, `resolve_project_or_fail`, `usage` | — | — | — |
| 35 | 2 | `cmd_daemon_logs` | 24476 | 29 | `abs_path_or_fail`, `lifecycle_trace_log_file`, `logs_dir_for_project`, `resolve_project_or_fail`, `runtime_events_log_file`, `usage` | — | — | — |
| 36 | 2 | `cmd_ensure_interruption_dispatch` | 24717 | 24 | `abs_path_or_fail`, `check_doc_gate_or_fail`, `cmd_ensure_interruption_dispatch_watch`, `ensure_interruption_dispatch_once`, `load_config`, `resolve_project_or_fail` … | — | — | — |
| 37 | 2 | `cmd_set_tool` | 21649 | 24 | `abs_path_or_fail`, `load_config`, `materialize_project_tooling_for_loaded_config`, `persist_project_tool_selection`, `resolve_project_or_fail`, `runtime_clear_session_state_for_fresh_launch` … | — | — | — |
| 38 | 2 | `cmd_intake_status` | 25847 | 27 | `abs_path_or_fail`, `count_active_intake_items`, `count_intake_items_by_status`, `intake_dir_for_project`, `intake_snapshot_for_project`, `resolve_project_or_fail` … | — | — | — |
| 39 | 2 | `cmd_restart` | 24230 | 21 | `abs_path_or_fail`, `cmd_global_restart`, `preflight_project_runtime_restart_or_fail`, `resolve_project_or_fail`, `start_project_runtime`, `startup_self_heal_machine_state_if_needed` … | — | — | — |
| 40 | 2 | `cmd_tui` | 25559 | 46 | `abs_path_or_fail`, `bootstrap_interruption_entry_runtime_or_fail`, `check_doc_gate_or_fail`, `render_tui_dashboard`, `resolve_project_or_fail`, `tui_compose_message` … | — | — | — |
| 41 | 2 | `cmd_intake_claim` | 25682 | 54 | `abs_path_or_fail`, `append_lifecycle_trace`, `intake_item_meta_file`, `resolve_project_or_fail`, `rewrite_existing_intake_item`, `usage` … | — | — | — |
| 42 | 2 | `cmd_task_mode` | 24518 | 56 | `abs_path_or_fail`, `ensure_task_mode_gate`, `load_config`, `read_task_mode`, `resolve_project_or_fail`, `stop_project_runtime` … | reason | — | — |
| 43 | 2 | `cmd_intake_chat` | 25605 | 77 | `_write_chat_to_issue`, `abs_path_or_fail`, `append_lifecycle_trace`, `intake_dir_for_project`, `next_intake_id`, `resolve_project_or_fail` … | — | — | — |
| 44 | 3 (last) | `cmd_ensure_manager` | 24661 | 41 | `abs_path_or_fail`, `check_doc_gate_or_fail`, `cmd_ensure_manager_watch`, `ensure_manager_once`, `load_config`, `main` … | — | — | — |
| 45 | 3 (last) | `cmd_doctor` | 24765 | 67 | `abs_path_or_fail`, `check_build_artifact_gate_or_fail`, `check_doc_gate_or_fail`, `check_execution_boundary_audit_or_fail`, `check_hook_gate_or_fail`, `check_supply_chain_gate_or_fail` … | — | — | — |
| 46 | 3 (last) | `cmd_init` | 21186 | 463 | `abs_path_or_fail`, `ensure_a2a_server_running`, `ensure_install_lifecycle_allowlist_file`, `ensure_project_agents_md`, `ensure_repo_hooks_enabled_or_fail`, `ensure_task_mode_gate` … | PROJECT_ROOT, reason | — | — |
| 47 | 3 (last) | `cmd_global_restart` | 22127 | 83 | `abs_path_or_fail`, `collect_global_restart_snapshot_rows`, `git_root_for_path`, `global_restart_history_retention`, `global_restart_manifest_dir`, `global_restart_manifest_history_dir` … | — | — | — |
| 48 | 3 (last) | `cmd_restore_work` | 24574 | 87 | `abs_path_or_fail`, `check_doc_gate_or_fail`, `count_active_intake_items`, `exit_contract_file`, `find_latest_prompt_file_for_project`, `latest_generated_manager_continuity_file_for_project` … | — | — | — |
| 49 | 3 (last) | `cmd_task_source_scan` | 26090 | 80 | `abs_path_or_fail`, `cmd_security_review_brief`, `freely_activation_consent_status_for_loaded_config`, `freely_execution_boundary_audit_detail_for_loaded_config`, `freely_execution_boundary_audit_status_for_loaded_config`, `freely_execution_boundary_audit_summary_for_loaded_config` … | CURRENT_TOOL_SLOT, LAST_ACTIVE_SLOT | — | — |
| 50 | 3 (last) | `cmd_intake_resolve` | 25736 | 111 | `abs_path_or_fail`, `append_lifecycle_trace`, `current_workcell_session_refs`, `intake_item_meta_file`, `load_config`, `load_session_state_or_defaults` … | CLASSIFICATION, DELEGATED_WORKTREE, LINKED_ARTIFACT, REACTION | — | — |
| 51 | 3 (last) | `cmd_develop_push` | 26880 | 117 | `abs_path_or_fail`, `branch_name_for_project`, `clear_develop_push_attempt_state`, `clear_develop_push_followthrough_state`, `develop_push_attempt_reason_from_output`, `develop_push_attempt_state_file` … | reason | — | — |
| 52 | 3 (last) | `cmd_start` | 24097 | 108 | `abs_path_or_fail`, `acquire_project_start_lock_or_wait`, `active_runtime_attach_reusable_for_project`, `append_lifecycle_trace`, `append_runtime_event`, `cmd_new_session` … | reason | issue-sync | — |
| 53 | 3 (last) | `cmd_daemon_start` | 24333 | 116 | `abs_path_or_fail`, `acquire_project_start_lock_or_wait`, `active_runtime_attach_reusable_for_project`, `append_lifecycle_trace`, `append_runtime_event`, `ensure_freely_db` … | LAST_EXIT_REASON, LAST_RESTART_STORM_COUNT, reason | — | — |
| 54 | 3 (last) | `cmd_fleet_status` | 26701 | 179 | `abs_path_or_fail`, `blocked_supervision_snapshot_for_project`, `checkpoint_guard_json_for_project`, `checkpoint_guard_value`, `config_file`, `develop_push_followthrough_snapshot_for_project` … | LAST_LAUNCH_KIND, LAST_MANAGER_WORKER_PROMPTS_CONSUMED, LAST_MANAGER_WORKER_PROMPTS_GENERATED, LAST_PROCESS_CHURN_PEAK … | — | — |
| 55 | 3 (last) | `cmd_baseline_status` | 25874 | 173 | `abs_path_or_fail`, `checkpoint_guard_json_for_project`, `checkpoint_guard_reason_codes`, `checkpoint_guard_value`, `count_active_intake_items`, `count_intake_items_by_status` … | ACTIVE_RUNNING_WORKER_COUNT, AVAILABLE_NEW_WORKER_SLOTS, CHECKPOINT_DRIFT_STREAK_CURRENT, CURRENT_TOOL_SLOT … | — | — |
| 56 | 3 (last) | `cmd_live_status` | 26170 | 418 | `abs_path_or_fail`, `blocked_supervision_snapshot_for_project`, `branch_name_for_project`, `count_intake_items_by_status`, `csv_retain_exact_items`, `develop_push_attempt_state_file` … | ACTIVE_RUNNING_WORKER_COUNT, AVAILABLE_NEW_WORKER_SLOTS, DESIRED_RUNTIME_STATE, LAST_AI_STATE … | — | — |

## 本轮（R31 第一阶段）完成的外移

| cmd | 行数 | 内部依赖 | 去向 |
|---|---|---|---|
| `cmd_test_gate_run` | 39 | `_test_gate_file` / `cmd_evidence_add` / `log_error` | `bin/test-gate run` |
| `cmd_test_gate_record` | 42 | `_test_gate_write` / `log_error` | `bin/test-gate record` |
| `cmd_evidence_add` | 22 | `log_error` | `bin/evidence add` |
| `_test_gate_file` / `_test_gate_write` | 4 / 14 | `run_dir_for_project` / `current_timestamp_utc_for_machine` | 同 `bin/test-gate` |

顺带把 4 个共用 helper（`_log_ts` / `log_info` / `log_warn` / `log_error`、`current_timestamp_utc_for_machine`、`state_dir`、`run_dir_for_project`）挪进 `runtime/lib/common.sh`，单体与 `bin/test-gate`、`bin/evidence` 同源引用 —— 这是后续每个 phase 1/2 外移的前置条件。

## 为什么是这个顺序

1. **phase 1 先做**：依赖 ≤3 的命令抽走后只剩 `exec` 一行，回归面最小，却能把「抽走后行为不变」的模式跑通（`bin/wt-create` 已验证过同一模式）。
2. **phase 2 需要先抽 helper**：这些命令依赖 4–8 个单体函数，直接抽会复制代码；先把 helper 归到 `runtime/lib/` 才能保持单源。
3. **phase 3 最后做**：daemon / dispatch / 状态机是宪法 §4 点名的核心面，也是唯一真正需要 Rust 的部分，先留原位、等 FFI 边界 PoC 有结论再动。

## 行数守卫

`bin/check-runtime-size` 读 `runtime/.size-budget`，超过即 fail-closed；只许下调，不许上调。`bin/check-file-size` 对这个文件是 `file-size: skip`，所以行数承诺必须由这个专用门禁承担。
