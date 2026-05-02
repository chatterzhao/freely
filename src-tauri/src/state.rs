use std::collections::HashMap;
use std::sync::Mutex;

use tauri::State;

use crate::model::{
    AgentInfo, ProjectSummary, RunInfo, SessionStatus, Snapshot, TerminalTarget,
};
use crate::validation_report::ValidationReportRecorder;

pub struct AppState {
    pub snapshots: Mutex<HashMap<String, Snapshot>>,
    pub validation_reporter: ValidationReportRecorder,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            snapshots: Mutex::new(HashMap::new()),
            validation_reporter: ValidationReportRecorder::default(),
        }
    }
}

pub fn default_session_id(project_id: &str) -> String {
    format!("{}-session-1", project_id)
}

pub fn default_run_id(project_id: &str) -> String {
    format!("{}-run-1", project_id)
}

pub fn default_terminal_target(project_id: &str) -> String {
    format!("{}:pty-0", default_run_id(project_id))
}

fn to_project_name(project_id: &str) -> String {
    project_id
        .split('-')
        .filter(|segment| !segment.is_empty())
        .map(|segment| {
            let mut chars = segment.chars();
            match chars.next() {
                Some(first) => format!("{}{}", first.to_ascii_uppercase(), chars.as_str()),
                None => String::new(),
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

pub fn default_snapshot(project_id: &str) -> Snapshot {
    let session_id = default_session_id(project_id);
    let run_id = default_run_id(project_id);

    Snapshot {
        project_summary: ProjectSummary {
            project_id: project_id.to_string(),
            project_name: to_project_name(project_id),
        },
        active_sessions: vec![SessionStatus {
            session_id: session_id.clone(),
            status: "running".to_string(),
        }],
        active_runs: vec![RunInfo {
            run_id: run_id.clone(),
            status: "in_dev".to_string(),
        }],
        active_agents: vec![AgentInfo {
            agent_id: "lead-agent".to_string(),
            phase: "dev_loop".to_string(),
            last_action: "awaiting command".to_string(),
            blocker: None,
        }],
        governance_summary: vec!["bridge connected".to_string()],
        recovery_summary: Vec::new(),
        last_event_id: "event-1".to_string(),
        terminal_targets: vec![TerminalTarget {
            terminal_target: default_terminal_target(project_id),
            session_id,
        }],
    }
}

pub fn with_snapshot<T>(
    state: &State<AppState>,
    project_id: &str,
    mutate: impl FnOnce(&mut Snapshot) -> T,
) -> T {
    let mut snapshots = state.snapshots.lock().expect("state mutex poisoned");
    let snapshot = snapshots
        .entry(project_id.to_string())
        .or_insert_with(|| default_snapshot(project_id));
    mutate(snapshot)
}

#[cfg(test)]
mod tests {
    use super::{default_snapshot, to_project_name};

    #[test]
    fn default_snapshot_uses_probe_contract_shape() {
        let snapshot = default_snapshot("freely");
        assert_eq!(snapshot.project_summary.project_id, "freely");
        assert_eq!(snapshot.project_summary.project_name, "Freely");
        assert_eq!(snapshot.last_event_id, "event-1");
        assert_eq!(snapshot.active_sessions.len(), 1);
        assert_eq!(snapshot.active_runs.len(), 1);
        assert_eq!(snapshot.active_agents.len(), 1);
        assert_eq!(snapshot.active_sessions[0].session_id, "freely-session-1");
        assert_eq!(snapshot.active_runs[0].run_id, "freely-run-1");
        assert_eq!(snapshot.terminal_targets[0].terminal_target, "freely-run-1:pty-0");
    }

    #[test]
    fn project_name_matches_frontend_title_case_rule() {
        assert_eq!(to_project_name("my-project"), "My Project");
        assert_eq!(to_project_name("freely"), "Freely");
    }
}
