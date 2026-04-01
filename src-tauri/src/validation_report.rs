use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use std::sync::Mutex;

use serde::Serialize;
use serde_json::Value;

use crate::model::{CommandAck, Snapshot};

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ValidationCommandRecord {
    pub command: String,
    pub ack_message: String,
    pub event_types: Vec<String>,
    pub last_event_id: String,
    pub active_run_status: Option<String>,
    pub active_session_id: Option<String>,
    pub governance_summary: Vec<String>,
}

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct ProjectValidationReport {
    pub project_id: String,
    pub status: String,
    pub observed_commands: Vec<String>,
    pub observed_event_types: Vec<String>,
    pub records: Vec<ValidationCommandRecord>,
}

pub struct ValidationReportRecorder {
    path: Option<PathBuf>,
    reports: Mutex<HashMap<String, ProjectValidationReport>>,
}

impl Default for ValidationReportRecorder {
    fn default() -> Self {
        Self {
            path: std::env::var_os("FREELY_PROBE_VALIDATION_REPORT_PATH").map(PathBuf::from),
            reports: Mutex::new(HashMap::new()),
        }
    }
}

impl ValidationReportRecorder {
    pub fn record_snapshot_request(
        &self,
        project_id: &str,
        snapshot: &Snapshot,
    ) -> Result<(), String> {
        let Some(path) = &self.path else {
            return Ok(());
        };

        let mut reports = self.reports.lock().expect("validation report mutex poisoned");
        let report = reports
            .entry(project_id.to_string())
            .or_insert_with(|| ProjectValidationReport {
                project_id: project_id.to_string(),
                status: "bootstrapped".to_string(),
                observed_commands: Vec::new(),
                observed_event_types: Vec::new(),
                records: Vec::new(),
            });

        if !report
            .observed_commands
            .iter()
            .any(|command| command == "RequestSnapshot")
        {
            report.observed_commands.push("RequestSnapshot".to_string());
        }
        if report.status != "passed" {
            report.status = "bootstrapped".to_string();
        }
        report.records.push(ValidationCommandRecord {
            command: "RequestSnapshot".to_string(),
            ack_message: "snapshot request accepted".to_string(),
            event_types: Vec::new(),
            last_event_id: snapshot.last_event_id.clone(),
            active_run_status: snapshot.active_runs.first().map(|run| run.status.clone()),
            active_session_id: snapshot
                .active_sessions
                .first()
                .map(|session| session.session_id.clone()),
            governance_summary: snapshot.governance_summary.clone(),
        });

        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|error| error.to_string())?;
        }
        let body = serde_json::to_vec_pretty(report).map_err(|error| error.to_string())?;
        fs::write(path, body).map_err(|error| error.to_string())
    }

    pub fn record_command(
        &self,
        project_id: &str,
        ack: &CommandAck,
        snapshot: &Snapshot,
        events: &[Value],
    ) -> Result<(), String> {
        let Some(path) = &self.path else {
            return Ok(());
        };

        let mut reports = self.reports.lock().expect("validation report mutex poisoned");
        let report = reports
            .entry(project_id.to_string())
            .or_insert_with(|| ProjectValidationReport {
                project_id: project_id.to_string(),
                status: "running".to_string(),
                observed_commands: Vec::new(),
                observed_event_types: Vec::new(),
                records: Vec::new(),
            });

        if !report.observed_commands.iter().any(|command| command == &ack.command) {
            report.observed_commands.push(ack.command.clone());
        }

        let event_types = events
            .iter()
            .filter_map(|event| {
                event
                    .get("type")
                    .and_then(Value::as_str)
                    .map(str::to_string)
            })
            .collect::<Vec<_>>();

        for event_type in &event_types {
            if !report
                .observed_event_types
                .iter()
                .any(|candidate| candidate == event_type)
            {
                report.observed_event_types.push(event_type.clone());
            }
        }

        report.records.push(ValidationCommandRecord {
            command: ack.command.clone(),
            ack_message: ack.message.clone(),
            event_types,
            last_event_id: snapshot.last_event_id.clone(),
            active_run_status: snapshot.active_runs.first().map(|run| run.status.clone()),
            active_session_id: snapshot
                .active_sessions
                .first()
                .map(|session| session.session_id.clone()),
            governance_summary: snapshot.governance_summary.clone(),
        });

        let required_commands = ["ControlRun", "CreateOrResumeSession", "SendChatIntervention"];
        let required_events = ["RunStatusChanged", "SessionUpserted", "InputArbitrationRecorded"];
        let commands_ready = required_commands.iter().all(|required| {
            report
                .observed_commands
                .iter()
                .any(|observed| observed == required)
        });
        let events_ready = required_events.iter().all(|required| {
            report
                .observed_event_types
                .iter()
                .any(|observed| observed == required)
        });
        report.status = if commands_ready && events_ready {
            "passed".to_string()
        } else {
            "running".to_string()
        };

        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).map_err(|error| error.to_string())?;
        }
        let body = serde_json::to_vec_pretty(report).map_err(|error| error.to_string())?;
        fs::write(path, body).map_err(|error| error.to_string())
    }
}
