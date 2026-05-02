pub const CONTRACT_VERSION: &str = "freely.probe.v1";
pub const PROBE_REQUEST_SNAPSHOT: &str = "probe_request_snapshot";
pub const PROBE_SEND_COMMAND: &str = "probe_send_command";
pub const PROBE_SERVER_EVENT: &str = "probe_server_event";

pub struct BridgeContract {
    pub contract_version: &'static str,
    pub request_snapshot_command: &'static str,
    pub send_command_command: &'static str,
    pub server_event_name: &'static str,
}

pub fn bridge_contract() -> BridgeContract {
    BridgeContract {
        contract_version: CONTRACT_VERSION,
        request_snapshot_command: PROBE_REQUEST_SNAPSHOT,
        send_command_command: PROBE_SEND_COMMAND,
        server_event_name: PROBE_SERVER_EVENT,
    }
}

#[cfg(test)]
mod tests {
    use serde_json::Value;

    use super::{
        bridge_contract, CONTRACT_VERSION, PROBE_REQUEST_SNAPSHOT, PROBE_SEND_COMMAND,
        PROBE_SERVER_EVENT,
    };

    #[test]
    fn rust_contract_matches_public_manifest() {
        let manifest: Value = serde_json::from_str(include_str!(
            "../../public/freely-probe-bridge-manifest.json"
        ))
        .expect("public manifest should be valid JSON");
        let contract = bridge_contract();

        assert_eq!(contract.contract_version, CONTRACT_VERSION);
        assert_eq!(
            manifest["contractVersion"].as_str(),
            Some(contract.contract_version)
        );
        assert_eq!(
            manifest["commands"]["requestSnapshot"]["commandName"].as_str(),
            Some(PROBE_REQUEST_SNAPSHOT)
        );
        assert_eq!(
            manifest["commands"]["sendCommand"]["commandName"].as_str(),
            Some(PROBE_SEND_COMMAND)
        );
        assert_eq!(
            manifest["events"]["serverEvent"]["eventName"].as_str(),
            Some(PROBE_SERVER_EVENT)
        );
    }
}
