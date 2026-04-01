#[derive(Debug, Clone)]
pub enum ProbeCommandKind {
    ControlRun,
    CreateOrResumeSession,
    AttachTerminal,
    SendChatIntervention,
    Other(String),
}

impl From<&str> for ProbeCommandKind {
    fn from(value: &str) -> Self {
        match value {
            "ControlRun" => Self::ControlRun,
            "CreateOrResumeSession" => Self::CreateOrResumeSession,
            "AttachTerminal" => Self::AttachTerminal,
            "SendChatIntervention" => Self::SendChatIntervention,
            other => Self::Other(other.to_string()),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::ProbeCommandKind;

    #[test]
    fn parses_known_commands() {
        assert!(matches!(
            ProbeCommandKind::from("ControlRun"),
            ProbeCommandKind::ControlRun
        ));
        assert!(matches!(
            ProbeCommandKind::from("CreateOrResumeSession"),
            ProbeCommandKind::CreateOrResumeSession
        ));
        assert!(matches!(
            ProbeCommandKind::from("AttachTerminal"),
            ProbeCommandKind::AttachTerminal
        ));
        assert!(matches!(
            ProbeCommandKind::from("SendChatIntervention"),
            ProbeCommandKind::SendChatIntervention
        ));
    }

    #[test]
    fn preserves_unknown_commands() {
        match ProbeCommandKind::from("CustomCommand") {
            ProbeCommandKind::Other(value) => assert_eq!(value, "CustomCommand"),
            _ => panic!("expected Other variant"),
        }
    }
}
