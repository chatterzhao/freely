use crate::command_kind::ProbeCommandKind;
use crate::command_payload::{
    parse_attach_terminal_payload, parse_chat_intervention_payload,
    parse_control_run_payload, parse_session_command_payload,
};
use crate::event_payload::{
    build_agent_status_event, build_audio_cue_event, build_input_arbitration_event,
    build_run_status_event, build_session_upserted_event, build_terminal_chunk_event,
};
use crate::model::{CommandAck, CommandEnvelope, SessionStatus, Snapshot};
use crate::state::{default_run_id, default_session_id};

pub struct AppliedCommand {
    pub ack: CommandAck,
    pub events: Vec<serde_json::Value>,
}

fn prepend_summary(summary: &mut Vec<String>, entry: impl Into<String>) {
    let mut next = vec![entry.into()];
    next.extend(summary.iter().cloned());
    next.truncate(4);
    *summary = next;
}

fn truncate_detail(value: Option<&str>) -> &str {
    match value {
        Some(value) if !value.is_empty() => value,
        _ => "probe-bridge",
    }
}

fn control_run_status(action: Option<&str>) -> &'static str {
    match action {
        Some("pause") => "paused",
        Some("terminate") => "terminated",
        Some("start") | Some("resume") | Some("retry") => "in_dev",
        _ => "in_dev",
    }
}

fn cue_lifecycle_for_action(action: Option<&str>) -> Option<&'static str> {
    match action {
        Some("start") | Some("resume") | Some("retry") => Some("started"),
        Some("terminate") => Some("completed"),
        _ => None,
    }
}

fn cue_actor_from_snapshot(snapshot: &Snapshot) -> &'static str {
    match snapshot.active_agents.first() {
        Some(agent) if agent.agent_id.starts_with("worker") => "worker",
        _ => "manager",
    }
}

fn next_event_id(last_event_id: &str) -> String {
    let next = last_event_id
        .rsplit_once('-')
        .and_then(|(_, suffix)| suffix.parse::<u64>().ok())
        .unwrap_or(0)
        + 1;
    format!("event-{}", next)
}

fn ack_message(
    command_kind: &ProbeCommandKind,
    control_action: Option<&str>,
    session_detail: Option<&str>,
    chat_detail: Option<&str>,
) -> String {
    match command_kind {
        ProbeCommandKind::ControlRun => format!(
            "control action accepted: {}",
            control_action.unwrap_or("unknown")
        ),
        ProbeCommandKind::CreateOrResumeSession => format!(
            "session accepted: {}",
            session_detail.unwrap_or("probe-ui")
        ),
        ProbeCommandKind::AttachTerminal => format!(
            "terminal attached: {}",
            session_detail.unwrap_or("unknown-target")
        ),
        ProbeCommandKind::SendChatIntervention => format!(
            "chat intervention accepted: {}",
            truncate_detail(chat_detail)
        ),
        ProbeCommandKind::Other(other) => format!("command accepted: {}", other),
    }
}

pub fn apply_command(
    snapshot: &mut Snapshot,
    project_id: &str,
    envelope: CommandEnvelope,
) -> AppliedCommand {
    let command_kind = ProbeCommandKind::from(envelope.command.as_str());
    let control_payload = parse_control_run_payload(&envelope.payload);
    let session_payload = parse_session_command_payload(&envelope.payload);
    let attach_payload = parse_attach_terminal_payload(&envelope.payload);
    let chat_payload = parse_chat_intervention_payload(&envelope.payload);
    snapshot.last_event_id = next_event_id(&snapshot.last_event_id);

    let events = match &command_kind {
        ProbeCommandKind::ControlRun => {
            let next_status = control_run_status(control_payload.action.as_deref()).to_string();
            let control_source = "human-control";
            let run_id = control_payload
                .run_id
                .clone()
                .or_else(|| snapshot.active_runs.first().map(|run| run.run_id.clone()))
                .unwrap_or_else(|| default_run_id(project_id));
            let control_reason = control_payload
                .reason
                .clone()
                .unwrap_or_else(|| "human-control".to_string());

            if let Some(run) = snapshot
                .active_runs
                .iter_mut()
                .find(|run| run.run_id == run_id)
            {
                run.status = next_status.clone();
            } else {
                snapshot.active_runs = vec![crate::model::RunInfo {
                    run_id: run_id.clone(),
                    status: next_status.clone(),
                }];
            }
            if let Some(target) = snapshot.terminal_targets.first_mut() {
                target.terminal_target = format!("{}:pty-0", run_id);
            }
            if let Some(agent) = snapshot.active_agents.first_mut() {
                agent.phase = "dev_loop".to_string();
                agent.last_action = format!(
                    "control:{}",
                    control_payload.action.as_deref().unwrap_or("unknown")
                );
                agent.blocker = if next_status == "paused" {
                    Some("paused by human-control".to_string())
                } else {
                    None
                };
            }
            if next_status == "paused" {
                prepend_summary(
                    &mut snapshot.recovery_summary,
                    format!("run {} paused by {}", run_id, control_reason),
                );
            } else {
                snapshot.recovery_summary.clear();
            }
            let mut events = vec![
                build_run_status_event(snapshot, project_id, control_source),
                build_agent_status_event(snapshot, project_id, control_source),
                build_terminal_chunk_event(
                    snapshot,
                    project_id,
                    format!(
                        "[rust:{}:{}] {} -> {}",
                        control_payload.action.as_deref().unwrap_or("unknown"),
                        control_reason,
                        run_id,
                        next_status
                    ),
                    control_source,
                ),
            ];
            if let Some(lifecycle) = cue_lifecycle_for_action(control_payload.action.as_deref()) {
                let actor = cue_actor_from_snapshot(snapshot);
                events.push(build_audio_cue_event(
                    snapshot,
                    project_id,
                    control_source,
                    Some(actor),
                    lifecycle,
                    &format!(
                        "run-{}",
                        control_payload.action.as_deref().unwrap_or("unknown")
                    ),
                ));
            }
            events
        }
        ProbeCommandKind::CreateOrResumeSession => {
            let session_source = session_payload
                .command_source
                .as_deref()
                .unwrap_or("human-control");
            let session_detail = session_payload
                .resume_hint
                .clone()
                .unwrap_or_else(|| "probe-ui".to_string());
            let session_id = session_payload
                .session_id
                .clone()
                .unwrap_or_else(|| default_session_id(project_id));
            snapshot.active_sessions = vec![SessionStatus {
                session_id: session_id.clone(),
                status: "running".to_string(),
            }];
            if let Some(target) = snapshot.terminal_targets.first_mut() {
                target.session_id = session_id;
            }
            prepend_summary(
                &mut snapshot.governance_summary,
                format!("session upserted via {}", session_detail),
            );
            vec![
                build_session_upserted_event(snapshot, project_id, session_source),
                build_audio_cue_event(
                    snapshot,
                    project_id,
                    session_source,
                    Some("manager"),
                    "started",
                    "session-created-or-resumed",
                ),
            ]
        }
        ProbeCommandKind::AttachTerminal => {
            let session_id = attach_payload
                .session_id
                .clone()
                .or_else(|| {
                    snapshot
                        .active_sessions
                        .first()
                        .map(|session| session.session_id.clone())
                })
                .unwrap_or_else(|| default_session_id(project_id));
            let run_id = attach_payload
                .run_id
                .clone()
                .or_else(|| snapshot.active_runs.first().map(|run| run.run_id.clone()))
                .unwrap_or_else(|| default_run_id(project_id));
            let terminal_target = attach_payload
                .terminal_target
                .clone()
                .unwrap_or_else(|| format!("{}:pty-0", run_id));

            snapshot.active_sessions = vec![SessionStatus {
                session_id: session_id.clone(),
                status: "running".to_string(),
            }];
            if let Some(run) = snapshot
                .active_runs
                .iter_mut()
                .find(|run| run.run_id == run_id)
            {
                run.status = "in_dev".to_string();
            } else {
                snapshot.active_runs = vec![crate::model::RunInfo {
                    run_id: run_id.clone(),
                    status: "in_dev".to_string(),
                }];
            }
            let mut next_terminal_targets = snapshot
                .terminal_targets
                .iter()
                .filter(|target| target.terminal_target != terminal_target)
                .cloned()
                .collect::<Vec<_>>();
            next_terminal_targets.insert(
                0,
                crate::model::TerminalTarget {
                    terminal_target: terminal_target.clone(),
                    session_id: session_id.clone(),
                },
            );
            snapshot.terminal_targets = next_terminal_targets;
            prepend_summary(
                &mut snapshot.governance_summary,
                format!("terminal attached to {}", terminal_target),
            );
            vec![build_terminal_chunk_event(
                snapshot,
                project_id,
                format!(
                    "[rust:attach:{}] session {} attached",
                    attach_payload.cursor.as_deref().unwrap_or("tail"),
                    session_id
                ),
                "human-control",
            )]
        }
        ProbeCommandKind::SendChatIntervention => {
            let chat_detail = truncate_detail(chat_payload.content.as_deref()).to_string();
            let message_id = chat_payload
                .message_id
                .clone()
                .unwrap_or_else(|| "message-unknown".to_string());
            let run_id = chat_payload
                .run_id
                .clone()
                .or_else(|| snapshot.active_runs.first().map(|run| run.run_id.clone()))
                .unwrap_or_else(|| default_run_id(project_id));
            let session_id = chat_payload
                .session_id
                .clone()
                .or_else(|| {
                    snapshot
                        .active_sessions
                        .first()
                        .map(|session| session.session_id.clone())
                })
                .unwrap_or_else(|| default_session_id(project_id));
            snapshot.active_sessions = vec![SessionStatus {
                session_id: session_id.clone(),
                status: "running".to_string(),
            }];
            if let Some(run) = snapshot
                .active_runs
                .iter_mut()
                .find(|run| run.run_id == run_id)
            {
                run.status = "in_dev".to_string();
            } else {
                snapshot.active_runs = vec![crate::model::RunInfo {
                    run_id: run_id.clone(),
                    status: "in_dev".to_string(),
                }];
            }
            if let Some(target) = snapshot.terminal_targets.first_mut() {
                target.terminal_target = format!("{}:pty-0", run_id);
                target.session_id = session_id.clone();
            }
            if let Some(agent) = snapshot.active_agents.first_mut() {
                if let Some(target_agent_id) = chat_payload.target_agent_id.as_deref() {
                    agent.agent_id = target_agent_id.to_string();
                }
                agent.last_action = format!("chat:{}", chat_detail);
            }
            prepend_summary(
                &mut snapshot.governance_summary,
                format!(
                    "chat intervention accepted for {} -> {}",
                    session_id, snapshot.active_agents[0].agent_id
                ),
            );
            let details = format!(
                "{} [{}] -> {} @ {}",
                chat_payload.content.as_deref().unwrap_or(""),
                message_id,
                snapshot.active_agents[0].agent_id,
                run_id
            );
            let mut events =
                vec![build_input_arbitration_event(snapshot, project_id, "human-chat", &details)];
            if snapshot.active_agents[0].agent_id.starts_with("worker") {
                events.push(build_audio_cue_event(
                    snapshot,
                    project_id,
                    "human-chat",
                    Some("worker"),
                    "started",
                    "worker-targeted-chat-intervention",
                ));
            }
            events
        }
        ProbeCommandKind::Other(_) => vec![build_terminal_chunk_event(
            snapshot,
            project_id,
            format!("unsupported command: {}", envelope.command),
            "system",
        )],
    };

    let ack = CommandAck {
        ok: true,
        command: envelope.command,
        project_id: project_id.to_string(),
        message: ack_message(
            &command_kind,
            control_payload.action.as_deref(),
            match &command_kind {
                ProbeCommandKind::AttachTerminal => attach_payload.terminal_target.as_deref(),
                _ => session_payload.resume_hint.as_deref(),
            },
            chat_payload.content.as_deref(),
        ),
    };

    AppliedCommand { ack, events }
}

#[cfg(test)]
mod contract_default_id_tests {
    use serde_json::json;

    use super::apply_command;
    use crate::model::CommandEnvelope;
    use crate::state::default_snapshot;

    #[test]
    fn create_or_resume_session_uses_contract_default_ids_and_updates_terminal_session() {
        let mut snapshot = default_snapshot("freely");
        snapshot.active_sessions.clear();
        snapshot.terminal_targets[0].session_id = "stale-session".to_string();

        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "CreateOrResumeSession".to_string(),
                payload: json!({
                    "projectId": "freely",
                    "type": "CreateOrResumeSession",
                    "resumeHint": "probe-ui"
                }),
            },
        );

        assert_eq!(applied.ack.message, "session accepted: probe-ui");
        assert_eq!(snapshot.active_sessions[0].session_id, "freely-session-1");
        assert_eq!(snapshot.terminal_targets[0].session_id, "freely-session-1");
        assert_eq!(applied.events[0]["sessionId"], "freely-session-1");
    }

    #[test]
    fn chat_intervention_uses_contract_default_ids_when_snapshot_is_empty() {
        let mut snapshot = default_snapshot("freely");
        snapshot.active_sessions.clear();
        snapshot.active_runs.clear();
        snapshot.terminal_targets.clear();

        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "SendChatIntervention".to_string(),
                payload: json!({
                    "projectId": "freely",
                    "type": "SendChatIntervention",
                    "messageId": "message-1",
                    "content": "hold here"
                }),
            },
        );

        assert_eq!(applied.ack.message, "chat intervention accepted: hold here");
        assert_eq!(snapshot.active_sessions[0].session_id, "freely-session-1");
        assert_eq!(snapshot.active_runs[0].run_id, "freely-run-1");
        assert_eq!(applied.events[0]["sessionId"], "freely-session-1");
        assert_eq!(applied.events[0]["details"], "hold here [message-1] -> lead-agent @ freely-run-1");
    }

    #[test]
    fn attach_terminal_updates_target_and_governance_summary() {
        let mut snapshot = default_snapshot("freely");

        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "AttachTerminal".to_string(),
                payload: json!({
                    "projectId": "freely",
                    "type": "AttachTerminal",
                    "sessionId": "freely-session-2",
                    "terminalTarget": "freely-run-2:pty-0",
                    "runId": "freely-run-2",
                    "cursor": "tail"
                }),
            },
        );

        assert_eq!(applied.ack.message, "terminal attached: freely-run-2:pty-0");
        assert_eq!(snapshot.active_sessions[0].session_id, "freely-session-2");
        assert_eq!(snapshot.active_runs[0].run_id, "freely-run-2");
        assert_eq!(snapshot.terminal_targets[0].terminal_target, "freely-run-2:pty-0");
        assert_eq!(snapshot.terminal_targets[0].session_id, "freely-session-2");
        assert_eq!(
            snapshot.governance_summary[0],
            "terminal attached to freely-run-2:pty-0"
        );
        assert_eq!(applied.events[0]["type"], "TerminalChunkAppended");
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::{apply_command, control_run_status, cue_lifecycle_for_action, prepend_summary};
    use crate::model::CommandEnvelope;
    use crate::state::default_snapshot;

    #[test]
    fn prepend_summary_keeps_latest_four_entries() {
        let mut summary = vec![
            "older-1".to_string(),
            "older-2".to_string(),
            "older-3".to_string(),
            "older-4".to_string(),
        ];

        prepend_summary(&mut summary, "latest");

        assert_eq!(summary, vec!["latest", "older-1", "older-2", "older-3"]);
    }

    #[test]
    fn maps_control_actions_to_expected_statuses() {
        assert_eq!(control_run_status(Some("start")), "in_dev");
        assert_eq!(control_run_status(Some("resume")), "in_dev");
        assert_eq!(control_run_status(Some("retry")), "in_dev");
        assert_eq!(control_run_status(Some("pause")), "paused");
        assert_eq!(control_run_status(Some("terminate")), "terminated");
    }

    #[test]
    fn maps_control_actions_to_audio_lifecycle() {
        assert_eq!(cue_lifecycle_for_action(Some("start")), Some("started"));
        assert_eq!(cue_lifecycle_for_action(Some("resume")), Some("started"));
        assert_eq!(cue_lifecycle_for_action(Some("retry")), Some("started"));
        assert_eq!(cue_lifecycle_for_action(Some("terminate")), Some("completed"));
        assert_eq!(cue_lifecycle_for_action(Some("pause")), None);
    }

    #[test]
    fn control_run_updates_snapshot_and_emits_run_event() {
        let mut snapshot = default_snapshot("freely");
        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "ControlRun".to_string(),
                payload: json!({"runId": "run-freely", "action": "start"}),
            },
        );

        assert_eq!(snapshot.last_event_id, "event-2");
        assert_eq!(snapshot.active_runs[0].status, "in_dev");
        assert_eq!(snapshot.active_agents[0].phase, "dev_loop");
        assert_eq!(applied.events.len(), 4);
        assert_eq!(applied.events[0]["type"], "RunStatusChanged");
        assert_eq!(applied.events[3]["type"], "AudioCueRequested");
        assert_eq!(applied.events[3]["cueKey"], "manager-started");
        assert_eq!(applied.ack.command, "ControlRun");
        assert_eq!(applied.ack.message, "control action accepted: start");
    }

    #[test]
    fn pause_updates_recovery_summary_and_blocker() {
        let mut snapshot = default_snapshot("freely");
        let _ = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "ControlRun".to_string(),
                payload: json!({"runId": "run-freely", "action": "pause"}),
            },
        );

        assert_eq!(snapshot.active_runs[0].status, "paused");
        assert_eq!(snapshot.recovery_summary, vec!["run run-freely paused by human-control"]);
        assert_eq!(
            snapshot.active_agents[0].blocker.as_deref(),
            Some("paused by human-control")
        );
    }

    #[test]
    fn session_upsert_prepends_governance_summary() {
        let mut snapshot = default_snapshot("freely");
        snapshot.governance_summary = vec![
            "older-1".to_string(),
            "older-2".to_string(),
            "older-3".to_string(),
            "older-4".to_string(),
        ];

        let _ = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "CreateOrResumeSession".to_string(),
                payload: json!({"sessionId": "session-dogfood", "resumeHint": "probe-ui"}),
            },
        );

        assert_eq!(
            snapshot.governance_summary,
            vec![
                "session upserted via probe-ui",
                "older-1",
                "older-2",
                "older-3"
            ]
        );
    }

    #[test]
    fn create_or_resume_session_adds_session_and_emits_session_event() {
        let mut snapshot = default_snapshot("freely");
        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "CreateOrResumeSession".to_string(),
                payload: json!({"sessionId": "session-dogfood", "resumeHint": "probe-ui"}),
            },
        );

        assert_eq!(snapshot.active_sessions.len(), 1);
        assert_eq!(snapshot.active_sessions[0].status, "running");
        assert_eq!(snapshot.active_sessions[0].session_id, "session-dogfood");
        assert_eq!(
            snapshot.governance_summary,
            vec!["session upserted via probe-ui", "bridge connected"]
        );
        assert_eq!(applied.events[0]["type"], "SessionUpserted");
        assert_eq!(applied.events[0]["source"], "human-control");
        assert_eq!(applied.events[1]["type"], "AudioCueRequested");
        assert_eq!(applied.events[1]["cueKey"], "manager-started");
        assert_eq!(applied.ack.message, "session accepted: probe-ui");
    }

    #[test]
    fn chat_intervention_uses_payload_content_in_snapshot() {
        let mut snapshot = default_snapshot("freely");
        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "SendChatIntervention".to_string(),
                payload: json!({
                    "sessionId": "session-2",
                    "messageId": "msg-1",
                    "content": "hold here",
                    "runId": "run-2",
                    "targetAgentId": "review-agent"
                }),
            },
        );

        assert_eq!(snapshot.active_sessions[0].session_id, "session-2");
        assert_eq!(snapshot.active_runs[0].run_id, "run-2");
        assert_eq!(snapshot.terminal_targets[0].terminal_target, "run-2:pty-0");
        assert_eq!(snapshot.active_agents[0].agent_id, "review-agent");
        assert_eq!(snapshot.active_agents[0].last_action, "chat:hold here");
        assert_eq!(
            snapshot.governance_summary,
            vec![
                "chat intervention accepted for session-2 -> review-agent",
                "bridge connected"
            ]
        );
        assert_eq!(applied.events[0]["type"], "InputArbitrationRecorded");
        assert_eq!(applied.events[0]["details"], "hold here [msg-1] -> review-agent @ run-2");
        assert_eq!(applied.ack.message, "chat intervention accepted: hold here");
    }

    #[test]
    fn worker_targeted_chat_emits_worker_started_audio_cue() {
        let mut snapshot = default_snapshot("freely");
        let applied = apply_command(
            &mut snapshot,
            "freely",
            CommandEnvelope {
                command: "SendChatIntervention".to_string(),
                payload: json!({
                    "sessionId": "session-2",
                    "messageId": "msg-1",
                    "content": "take this lane",
                    "runId": "run-2",
                    "targetAgentId": "worker-2"
                }),
            },
        );

        assert_eq!(applied.events.len(), 2);
        assert_eq!(applied.events[1]["type"], "AudioCueRequested");
        assert_eq!(applied.events[1]["cueKey"], "worker-started");
    }
}
