#[derive(Debug, Clone)]
pub enum ProbeEventKind {
    RunStatusChanged,
    AgentStatusChanged,
    SessionUpserted,
    InputArbitrationRecorded,
    TerminalChunkAppended,
}

impl ProbeEventKind {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::RunStatusChanged => "RunStatusChanged",
            Self::AgentStatusChanged => "AgentStatusChanged",
            Self::SessionUpserted => "SessionUpserted",
            Self::InputArbitrationRecorded => "InputArbitrationRecorded",
            Self::TerminalChunkAppended => "TerminalChunkAppended",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::ProbeEventKind;

    #[test]
    fn exposes_expected_event_names() {
        assert_eq!(
            ProbeEventKind::RunStatusChanged.as_str(),
            "RunStatusChanged"
        );
        assert_eq!(ProbeEventKind::SessionUpserted.as_str(), "SessionUpserted");
        assert_eq!(
            ProbeEventKind::InputArbitrationRecorded.as_str(),
            "InputArbitrationRecorded"
        );
        assert_eq!(
            ProbeEventKind::TerminalChunkAppended.as_str(),
            "TerminalChunkAppended"
        );
    }
}
