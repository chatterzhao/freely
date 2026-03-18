use serde_json::Value;
use tauri::{AppHandle, Emitter, State};

mod bridge_manifest;
mod bridge_logic;
mod command_kind;
mod command_payload;
mod event_kind;
mod event_payload;
mod model;
mod state;

use bridge_logic::apply_command;
use bridge_manifest::{bridge_contract, PROBE_SERVER_EVENT};
use model::{CommandAck, CommandEnvelope, Snapshot};
use state::{with_snapshot, AppState};

fn parse_project_id(payload: &Value) -> Result<String, String> {
    payload
        .get("projectId")
        .or_else(|| payload.get("project_id"))
        .and_then(|value| value.as_str())
        .map(str::to_string)
        .ok_or_else(|| "missing projectId".to_string())
}

fn emit_server_event(app: &AppHandle, event: Value) -> Result<(), String> {
    app.emit(PROBE_SERVER_EVENT, event)
        .map_err(|error| error.to_string())
}

#[tauri::command]
fn probe_request_snapshot(payload: Value, state: State<AppState>) -> Result<Snapshot, String> {
    let project_id = parse_project_id(&payload)?;
    Ok(with_snapshot(&state, &project_id, |snapshot| snapshot.clone()))
}

#[tauri::command]
fn probe_send_command(
    app: AppHandle,
    command: Value,
    state: State<AppState>,
) -> Result<CommandAck, String> {
    let project_id = parse_project_id(&command)?;
    let command_type = command
        .get("type")
        .and_then(|value| value.as_str())
        .ok_or_else(|| "missing command.type".to_string())?
        .to_string();

    let applied = with_snapshot(&state, &project_id, |snapshot| {
        apply_command(
            snapshot,
            &project_id,
            CommandEnvelope {
                command: command_type,
                payload: command,
            },
        )
    });

    for event in applied.events {
        emit_server_event(&app, event)?;
    }

    Ok(applied.ack)
}

pub fn run() {
    let contract = bridge_contract();
    debug_assert_eq!(contract.contract_version, "freely.probe.v1");
    debug_assert_eq!(contract.request_snapshot_command, "probe_request_snapshot");
    debug_assert_eq!(contract.send_command_command, "probe_send_command");
    debug_assert_eq!(contract.server_event_name, PROBE_SERVER_EVENT);

    tauri::Builder::default()
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![
            probe_request_snapshot,
            probe_send_command
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::parse_project_id;

    #[test]
    fn parses_camel_case_project_id() {
        assert_eq!(
            parse_project_id(&json!({ "projectId": "freely" })).as_deref(),
            Ok("freely")
        );
    }

    #[test]
    fn also_accepts_legacy_snake_case_project_id() {
        assert_eq!(
            parse_project_id(&json!({ "project_id": "freely" })).as_deref(),
            Ok("freely")
        );
    }
}
