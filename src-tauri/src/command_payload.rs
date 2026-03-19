use serde_json::Value;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlRunPayload {
    pub run_id: Option<String>,
    pub action: Option<String>,
    pub reason: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SessionCommandPayload {
    pub session_id: Option<String>,
    pub resume_hint: Option<String>,
    pub command_source: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChatInterventionPayload {
    pub session_id: Option<String>,
    pub message_id: Option<String>,
    pub content: Option<String>,
    pub run_id: Option<String>,
    pub target_agent_id: Option<String>,
}

pub fn parse_control_run_payload(payload: &Value) -> ControlRunPayload {
    ControlRunPayload {
        run_id: payload
            .get("runId")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        action: payload
            .get("action")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        reason: payload
            .get("reason")
            .and_then(|value| value.as_str())
            .map(str::to_string),
    }
}

pub fn parse_session_command_payload(payload: &Value) -> SessionCommandPayload {
    SessionCommandPayload {
        session_id: payload
            .get("sessionId")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        resume_hint: payload
            .get("resumeHint")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        command_source: payload
            .get("commandSource")
            .and_then(|value| value.as_str())
            .map(str::to_string),
    }
}

pub fn parse_chat_intervention_payload(payload: &Value) -> ChatInterventionPayload {
    ChatInterventionPayload {
        session_id: payload
            .get("sessionId")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        message_id: payload
            .get("messageId")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        content: payload
            .get("content")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        run_id: payload
            .get("runId")
            .and_then(|value| value.as_str())
            .map(str::to_string),
        target_agent_id: payload
            .get("targetAgentId")
            .and_then(|value| value.as_str())
            .map(str::to_string),
    }
}

#[cfg(test)]
mod tests {
    use serde_json::json;

    use super::{
        parse_chat_intervention_payload, parse_control_run_payload, parse_session_command_payload,
    };

    #[test]
    fn parses_control_run_fields() {
        let payload = parse_control_run_payload(&json!({
            "runId": "run-1",
            "action": "pause",
            "reason": "human override"
        }));
        assert_eq!(payload.run_id.as_deref(), Some("run-1"));
        assert_eq!(payload.action.as_deref(), Some("pause"));
        assert_eq!(payload.reason.as_deref(), Some("human override"));
    }

    #[test]
    fn parses_session_fields() {
        let payload = parse_session_command_payload(&json!({
            "sessionId": "session-1",
            "resumeHint": "probe-ui",
            "commandSource": "human-control"
        }));
        assert_eq!(payload.session_id.as_deref(), Some("session-1"));
        assert_eq!(payload.resume_hint.as_deref(), Some("probe-ui"));
        assert_eq!(payload.command_source.as_deref(), Some("human-control"));
    }

    #[test]
    fn parses_chat_fields() {
        let payload = parse_chat_intervention_payload(&json!({
            "sessionId": "session-1",
            "messageId": "message-1",
            "content": "hold here",
            "runId": "run-1",
            "targetAgentId": "lead-agent"
        }));
        assert_eq!(payload.session_id.as_deref(), Some("session-1"));
        assert_eq!(payload.message_id.as_deref(), Some("message-1"));
        assert_eq!(payload.content.as_deref(), Some("hold here"));
        assert_eq!(payload.run_id.as_deref(), Some("run-1"));
        assert_eq!(payload.target_agent_id.as_deref(), Some("lead-agent"));
    }
}
