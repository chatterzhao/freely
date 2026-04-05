use serde_json::Value;
use time::OffsetDateTime;
use time::format_description::well_known::Rfc3339;

use crate::event_kind::ProbeEventKind;
use crate::model::Snapshot;
use crate::state::{default_run_id, default_session_id, default_terminal_target};

fn occurred_at_now() -> String {
    OffsetDateTime::now_utc()
        .format(&Rfc3339)
        .unwrap_or_else(|_| "1970-01-01T00:00:00Z".to_string())
}

fn base_event(
    snapshot: &Snapshot,
    project_id: &str,
    event_type: &str,
    source: &str,
) -> serde_json::Map<String, Value> {
    let mut event = serde_json::Map::new();
    event.insert("type".to_string(), Value::String(event_type.to_string()));
    event.insert(
        "eventId".to_string(),
        Value::String(snapshot.last_event_id.clone()),
    );
    event.insert(
        "occurredAt".to_string(),
        Value::String(occurred_at_now()),
    );
    event.insert(
        "projectId".to_string(),
        Value::String(project_id.to_string()),
    );
    event.insert(
        "sessionId".to_string(),
        Value::String(
            snapshot
                .active_sessions
                .first()
                .map(|session| session.session_id.clone())
                .unwrap_or_else(|| default_session_id(project_id)),
        ),
    );
    event.insert("source".to_string(), Value::String(source.to_string()));
    event
}

fn cue_key(actor: &str, lifecycle: &str) -> String {
    format!("{}-{}", actor, lifecycle)
}

fn primary_actor(snapshot: &Snapshot) -> &'static str {
    let Some(agent) = snapshot.active_agents.first() else {
        return "manager";
    };

    if agent.agent_id.starts_with("worker") {
        "worker"
    } else {
        "manager"
    }
}

pub fn build_session_upserted_event(snapshot: &Snapshot, project_id: &str, source: &str) -> Value {
    let mut event = base_event(
        snapshot,
        project_id,
        ProbeEventKind::SessionUpserted.as_str(),
        source,
    );
    let status = snapshot
        .active_sessions
        .first()
        .map(|session| session.status.clone())
        .unwrap_or_else(|| "running".to_string());
    event.insert("status".to_string(), Value::String(status));
    Value::Object(event)
}

pub fn build_input_arbitration_event(
    snapshot: &Snapshot,
    project_id: &str,
    source: &str,
    detail: &str,
) -> Value {
    let mut event = base_event(
        snapshot,
        project_id,
        ProbeEventKind::InputArbitrationRecorded.as_str(),
        source,
    );
    event.insert("outcome".to_string(), Value::String("accepted".to_string()));
    event.insert("details".to_string(), Value::String(detail.to_string()));
    Value::Object(event)
}

pub fn build_run_status_event(snapshot: &Snapshot, project_id: &str, source: &str) -> Value {
    let mut event = base_event(
        snapshot,
        project_id,
        ProbeEventKind::RunStatusChanged.as_str(),
        source,
    );
    let run = snapshot.active_runs.first().cloned();
    event.insert(
        "runId".to_string(),
        Value::String(
            run.as_ref()
                .map(|run| run.run_id.clone())
                .unwrap_or_else(|| default_run_id(project_id)),
        ),
    );
    event.insert(
        "status".to_string(),
        Value::String(
            run.map(|run| run.status)
                .unwrap_or_else(|| "in_dev".to_string()),
        ),
    );
    Value::Object(event)
}

pub fn build_agent_status_event(snapshot: &Snapshot, project_id: &str, source: &str) -> Value {
    let mut event = base_event(
        snapshot,
        project_id,
        ProbeEventKind::AgentStatusChanged.as_str(),
        source,
    );
    let agent = snapshot.active_agents.first().cloned();
    event.insert(
        "agentId".to_string(),
        Value::String(
            agent
                .as_ref()
                .map(|agent| agent.agent_id.clone())
                .unwrap_or_else(|| "lead-agent".to_string()),
        ),
    );
    event.insert(
        "phase".to_string(),
        Value::String(
            agent
                .as_ref()
                .map(|agent| agent.phase.clone())
                .unwrap_or_else(|| "dev_loop".to_string()),
        ),
    );
    event.insert(
        "lastAction".to_string(),
        Value::String(
            agent
                .map(|agent| agent.last_action)
                .unwrap_or_else(|| "awaiting command".to_string()),
        ),
    );
    Value::Object(event)
}

pub fn build_terminal_chunk_event(
    snapshot: &Snapshot,
    project_id: &str,
    chunk: String,
    source: &str,
) -> Value {
    let mut event = base_event(
        snapshot,
        project_id,
        ProbeEventKind::TerminalChunkAppended.as_str(),
        source,
    );
    event.insert(
        "terminalTarget".to_string(),
        Value::String(
            snapshot
                .terminal_targets
                .first()
                .map(|target| target.terminal_target.clone())
                .unwrap_or_else(|| default_terminal_target(project_id)),
        ),
    );
    event.insert("chunk".to_string(), Value::String(chunk));
    Value::Object(event)
}

pub fn build_audio_cue_event(
    snapshot: &Snapshot,
    project_id: &str,
    source: &str,
    actor: Option<&str>,
    lifecycle: &str,
    reason: &str,
) -> Value {
    let actor = actor.unwrap_or_else(|| primary_actor(snapshot));
    let mut event = base_event(
        snapshot,
        project_id,
        ProbeEventKind::AudioCueRequested.as_str(),
        source,
    );
    event.insert(
        "cueKey".to_string(),
        Value::String(cue_key(actor, lifecycle)),
    );
    event.insert("actor".to_string(), Value::String(actor.to_string()));
    event.insert(
        "lifecycle".to_string(),
        Value::String(lifecycle.to_string()),
    );
    event.insert("reason".to_string(), Value::String(reason.to_string()));
    Value::Object(event)
}

#[cfg(test)]
mod tests {
    use super::{
        build_audio_cue_event, build_input_arbitration_event, build_run_status_event,
        build_session_upserted_event, build_terminal_chunk_event,
    };
    use crate::model::{ProjectSummary, Snapshot};
    use crate::state::default_snapshot;

    #[test]
    fn builds_session_event_with_frontend_shape() {
        let snapshot = default_snapshot("freely");
        let event = build_session_upserted_event(&snapshot, "freely", "human-control");
        assert_eq!(event["type"], "SessionUpserted");
        assert_eq!(event["sessionId"], "freely-session-1");
        assert_eq!(event["status"], "running");
    }

    #[test]
    fn builds_run_event_with_frontend_shape() {
        let snapshot = default_snapshot("freely");
        let event = build_run_status_event(&snapshot, "freely", "human-control");
        assert_eq!(event["type"], "RunStatusChanged");
        assert_eq!(event["runId"], "freely-run-1");
        assert_eq!(event["status"], "in_dev");
    }

    #[test]
    fn builds_input_arbitration_event_with_details() {
        let snapshot = default_snapshot("freely");
        let event = build_input_arbitration_event(&snapshot, "freely", "human-chat", "hold here");
        assert_eq!(event["type"], "InputArbitrationRecorded");
        assert_eq!(event["outcome"], "accepted");
        assert_eq!(event["details"], "hold here");
        let occurred_at = event["occurredAt"].as_str().expect("occurredAt should be a string");
        assert!(occurred_at.contains('T'));
        assert!(occurred_at.ends_with('Z'));
    }

    #[test]
    fn uses_current_default_fallback_ids_when_snapshot_lists_are_empty() {
        let snapshot = Snapshot {
            project_summary: ProjectSummary {
                project_id: "freely".to_string(),
                project_name: "Freely".to_string(),
            },
            active_sessions: Vec::new(),
            active_runs: Vec::new(),
            active_agents: Vec::new(),
            governance_summary: Vec::new(),
            recovery_summary: Vec::new(),
            last_event_id: "event-1".to_string(),
            terminal_targets: Vec::new(),
        };

        let run_event = build_run_status_event(&snapshot, "freely", "human-control");
        let terminal_event =
            build_terminal_chunk_event(&snapshot, "freely", "chunk".to_string(), "system");

        assert_eq!(run_event["sessionId"], "freely-session-1");
        assert_eq!(run_event["runId"], "freely-run-1");
        assert_eq!(terminal_event["terminalTarget"], "freely-run-1:pty-0");
    }

    #[test]
    fn builds_audio_cue_event_with_actor_and_lifecycle() {
        let snapshot = default_snapshot("freely");
        let event = build_audio_cue_event(
            &snapshot,
            "freely",
            "system",
            Some("worker"),
            "completed",
            "run-terminate",
        );

        assert_eq!(event["type"], "AudioCueRequested");
        assert_eq!(event["cueKey"], "worker-completed");
        assert_eq!(event["actor"], "worker");
        assert_eq!(event["lifecycle"], "completed");
        assert_eq!(event["reason"], "run-terminate");
    }
}
