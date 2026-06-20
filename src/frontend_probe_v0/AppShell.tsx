import type { ProbeAdapter } from "./adapter";
import type { ServerEvent } from "./contracts";
import { buildPanelModels } from "./panels";
import { useState, useEffect } from "react";

import { useProbeChatIntervention } from "./useProbeChatIntervention";
import { useProbeEvents } from "./useProbeEvents";
import { useProbeControls } from "./useProbeControls";
import { useProbeSessionLifecycle } from "./useProbeSessionLifecycle";
import { useProbeTerminalAttach } from "./useProbeTerminalAttach";
import { useAudioNotifier } from "./useAudioNotifier";
import { formatTimestampForDisplay, getSystemTimeZone } from "./timeDisplay";
import { useTauriValidationSequence } from "./useTauriValidationSequence";
import { useProbeRuntime } from "./useProbeRuntime";

const appShellStyle: Record<string, string | number> = {
  minHeight: "100vh",
  background:
    "linear-gradient(160deg, #f4efe3 0%, #d5e6df 45%, #f9f5ec 100%)",
  color: "#17211f",
  fontFamily: '"Iowan Old Style", "Palatino Linotype", serif',
  padding: "32px",
};

const gridStyle: Record<string, string | number> = {
  display: "grid",
  gap: "16px",
  gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
  marginTop: "24px",
};

const cardStyle: Record<string, string | number> = {
  background: "rgba(255, 252, 245, 0.88)",
  border: "1px solid rgba(23, 33, 31, 0.12)",
  borderRadius: "18px",
  padding: "18px",
  boxShadow: "0 10px 30px rgba(23, 33, 31, 0.08)",
};

const sectionTitleStyle: Record<string, string | number> = {
  fontSize: "0.8rem",
  letterSpacing: "0.08em",
  marginBottom: "8px",
  marginTop: "14px",
  textTransform: "uppercase",
};

const listStyle: Record<string, string | number> = {
  display: "grid",
  gap: "8px",
  listStyle: "none",
  margin: 0,
  padding: 0,
};

const listItemStyle: Record<string, string | number> = {
  background: "rgba(23, 33, 31, 0.05)",
  borderRadius: "12px",
  padding: "10px 12px",
};

function describeEvent(event: ServerEvent) {
  switch (event.type) {
    case "SessionUpserted":
      return `${event.type} · ${event.source} · ${event.sessionId} -> ${event.status}`;
    case "RunStatusChanged":
      return `${event.type} · ${event.source} · ${event.runId} -> ${event.status}`;
    case "AgentStatusChanged":
      return `${event.type} · ${event.source} · ${event.agentId} -> ${event.lastAction}`;
    case "TerminalChunkAppended":
      return `${event.type} · ${event.source} · ${event.chunk}`;
    case "InputArbitrationRecorded":
      return `${event.type} · ${event.source} · ${event.outcome} · ${event.details}`;
    case "GovernanceDecisionRecorded":
      return `${event.type} · ${event.source} · ${event.decision}`;
    case "RecoveryStatusChanged":
      return `${event.type} · ${event.source} · ${event.runtimeState}`;
    case "AudioCueRequested":
      return `${event.type} · ${event.actor} · ${event.lifecycle} · ${event.reason}`;
  }
}

export type AppShellProps = {
  adapter?: ProbeAdapter;
  bridgeContractVersion?: string;
  projectId?: string;
  runtimeMode?: "mock" | "tauri";
  transportMode?: "mock" | "tauri-mock" | "tauri-broken";
  validationMode?: "off" | "tauri-smoke";
  bridgeBindings?: {
    requestSnapshotCommand: string;
    sendCommandCommand: string;
    serverEventName: string;
  };
};

export function AppShell({
  adapter,
  bridgeContractVersion,
  projectId = "freely",
  runtimeMode = "mock",
  transportMode = "mock",
  validationMode = "off",
  bridgeBindings,
}: AppShellProps) {
  const [selectedProjectId, setSelectedProjectId] = useState(projectId);
  const [projectList, setProjectList] = useState<string[]>([]);

  useEffect(() => {
    if (!adapter) return;
    let cancelled = false;
    adapter.listProjects().then((ids) => {
      if (!cancelled) setProjectList(ids);
    });
    return () => { cancelled = true; };
  }, [adapter]);

  const { adapter: resolvedAdapter, error: runtimeError, snapshot, loading } = useProbeRuntime(
    selectedProjectId,
    adapter,
  );
  const panels = snapshot ? buildPanelModels(snapshot) : [];
  const activeRun = snapshot?.activeRuns[0];
  const controls = useProbeControls(
    selectedProjectId,
    activeRun?.runId,
    resolvedAdapter,
  );
  const events = useProbeEvents(resolvedAdapter);
  const validation = useTauriValidationSequence({
    adapter: resolvedAdapter,
    events,
    projectId: selectedProjectId,
    runtimeMode,
    snapshot,
    validationMode,
  });
  const chat = useProbeChatIntervention(
    selectedProjectId,
    snapshot?.activeSessions[0]?.sessionId,
    activeRun?.runId,
    resolvedAdapter,
  );
  const sessionLifecycle = useProbeSessionLifecycle(
    selectedProjectId,
    snapshot?.activeSessions[0]?.sessionId,
    resolvedAdapter,
  );
  const terminalAttach = useProbeTerminalAttach(
    selectedProjectId,
    snapshot?.activeSessions[0]?.sessionId,
    activeRun?.runId,
    snapshot?.terminalTargets ?? [],
    resolvedAdapter,
  );
  const recentTerminalEvents = events
    .filter(
      (
        event,
      ): event is Extract<ServerEvent, { type: "TerminalChunkAppended" }> =>
        event.type === "TerminalChunkAppended" &&
        (!terminalAttach.attachedTarget ||
          event.terminalTarget === terminalAttach.attachedTarget),
    )
    .slice(-3)
    .reverse();
  const recentDecisionEvents = events
    .filter(
      (event) =>
        event.type === "InputArbitrationRecorded" ||
        event.type === "GovernanceDecisionRecorded",
    )
    .slice(-3)
    .reverse();
  const recentEvents = events.slice(-5).reverse();
  const systemTimeZone = getSystemTimeZone();
  const audioState = useAudioNotifier(resolvedAdapter);
  const updateTransportMode = (nextTransportMode: "mock" | "tauri-mock" | "tauri-broken") => {
    const url = new URL(window.location.href);
    if (nextTransportMode === "mock") {
      url.searchParams.delete("transport");
    } else {
      url.searchParams.set("transport", nextTransportMode);
    }
    window.location.assign(url.toString());
  };

  return (
    <main style={appShellStyle}>
      <header>
        <p style={{ letterSpacing: "0.08em", textTransform: "uppercase" }}>
          Frontend Probe v0
        </p>
        <h1 style={{ fontSize: "clamp(2rem, 5vw, 4rem)", margin: 0 }}>
          Freely Team Console
        </h1>
        <p style={{ fontSize: "1.1rem", marginBottom: 0 }}>
          {snapshot?.projectSummary.projectName ?? "Loading project..."}
        </p>
        <p style={{ maxWidth: "56ch", lineHeight: 1.5 }}>
          A minimal probe shell that keeps the control bar, chat intervention,
          agent roster, and embedded terminal visible through a single snapshot
          surface.
        </p>
        <label style={{ display: "grid", gap: "6px", marginTop: "16px", maxWidth: "280px" }}>
          <span style={{ letterSpacing: "0.08em", textTransform: "uppercase" }}>
            Project Switch
          </span>
          <select
            onChange={(event) => setSelectedProjectId(event.target.value)}
            style={{
              border: "1px solid rgba(23, 33, 31, 0.18)",
              borderRadius: "12px",
              font: "inherit",
              padding: "10px 12px",
            }}
            value={selectedProjectId}
          >
            {(projectList.length > 0 ? projectList : [projectId]).map((candidateProjectId) => (
              <option key={candidateProjectId} value={candidateProjectId}>
                {candidateProjectId}
              </option>
            ))}
          </select>
        </label>
        <label style={{ display: "grid", gap: "6px", marginTop: "16px", maxWidth: "280px" }}>
          <span style={{ letterSpacing: "0.08em", textTransform: "uppercase" }}>
            Transport
          </span>
          <select
            onChange={(event) =>
              updateTransportMode(
                event.target.value as "mock" | "tauri-mock" | "tauri-broken",
              )
            }
            style={{
              border: "1px solid rgba(23, 33, 31, 0.18)",
              borderRadius: "12px",
              font: "inherit",
              padding: "10px 12px",
            }}
            value={transportMode}
          >
            {["mock", "tauri-mock", "tauri-broken"].map((candidateTransportMode) => (
              <option key={candidateTransportMode} value={candidateTransportMode}>
                {candidateTransportMode}
              </option>
            ))}
          </select>
        </label>
        <p>
          {loading
            ? "Loading snapshot..."
            : `Loaded ${snapshot?.activeRuns.length ?? 0} run(s) from the probe adapter for ${selectedProjectId}.`}
        </p>
        <p>{`Buffered event count: ${events.length}`}</p>
        <p>{`Audio cue status: ${audioState.status}`}</p>
        <p>{`Last event id: ${snapshot?.lastEventId ?? "n/a"}`}</p>
        <p>{`Display timezone: ${systemTimeZone}`}</p>
        <p>{`Runtime mode: ${runtimeMode}`}</p>
        <p>{`Validation mode: ${validationMode}`}</p>
        <p>{`Bridge contract: ${bridgeContractVersion ?? "n/a"}`}</p>
        <p>
          {`Bridge: ${bridgeBindings?.requestSnapshotCommand ?? "n/a"} / ${
            bridgeBindings?.sendCommandCommand ?? "n/a"
          } / ${bridgeBindings?.serverEventName ?? "n/a"}`}
        </p>
        {runtimeError ? (
          <p
            style={{
              ...listItemStyle,
              border: "1px solid rgba(163, 49, 49, 0.18)",
              color: "#7b1f1f",
            }}
          >
            {`Runtime error: ${runtimeError}`}
          </p>
        ) : null}
        <div style={{ display: "grid", gap: "12px", marginTop: "16px", maxWidth: "720px" }}>
          <div>
            <p style={sectionTitleStyle}>Governance Summary</p>
            <ul style={listStyle}>
              {(snapshot?.governanceSummary ?? []).map((summary) => (
                <li key={summary} style={listItemStyle}>
                  {summary}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <p style={sectionTitleStyle}>Recovery Summary</p>
            <ul style={listStyle}>
              {(snapshot?.recoverySummary?.length ?? 0) > 0 ? (
                snapshot?.recoverySummary.map((summary) => (
                  <li key={summary} style={listItemStyle}>
                    {summary}
                  </li>
                ))
              ) : (
                <li style={listItemStyle}>No recovery events recorded for this project.</li>
              )}
            </ul>
          </div>
          {validationMode !== "off" ? (
            <div>
              <p style={sectionTitleStyle}>Validation Report</p>
              <ul style={listStyle}>
                <li style={listItemStyle}>{`status: ${validation.status}`}</li>
                <li style={listItemStyle}>{`start: ${validation.steps.start}`}</li>
                <li style={listItemStyle}>{`session: ${validation.steps.session}`}</li>
                <li style={listItemStyle}>{`attach: ${validation.steps.attach}`}</li>
                <li style={listItemStyle}>{`chat: ${validation.steps.chat}`}</li>
                <li style={listItemStyle}>{`error: ${validation.error ?? "none"}`}</li>
              </ul>
            </div>
          ) : null}
          <div>
            <p style={sectionTitleStyle}>Recent Activity</p>
            <ul style={listStyle}>
              {recentEvents.length > 0 ? (
                recentEvents.map((event) => (
                  <li key={event.eventId} style={listItemStyle}>
                    {describeEvent(event)}
                    <div title={event.occurredAt}>
                      {formatTimestampForDisplay(event.occurredAt)}
                    </div>
                  </li>
                ))
              ) : (
                <li style={listItemStyle}>No recent activity for this project.</li>
              )}
            </ul>
          </div>
        </div>
      </header>

      <section style={gridStyle}>
        {panels.map((panel) => (
          <article key={panel.id} style={cardStyle}>
            <h2 style={{ marginTop: 0 }}>{panel.title}</h2>
            <p>{panel.summary}</p>
            {panel.id === "control-bar" ? (
              <>
                <p style={sectionTitleStyle}>Current Run</p>
                <ul style={listStyle}>
                  <li style={listItemStyle}>
                    {activeRun
                      ? `${activeRun.runId} · ${activeRun.status}`
                      : "No active run in snapshot"}
                  </li>
                </ul>
                <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginTop: "12px" }}>
                  {["start", "pause", "terminate", "resume", "retry"].map((action) => (
                    <button
                      key={action}
                      disabled={!activeRun}
                      onClick={() =>
                        controls.trigger(
                          action as "start" | "pause" | "terminate" | "resume" | "retry",
                        )
                      }
                      style={{
                        borderRadius: "999px",
                        border: "1px solid rgba(23, 33, 31, 0.18)",
                        background: activeRun ? "#fff7e8" : "#efe9dc",
                        opacity: activeRun ? 1 : 0.55,
                        padding: "8px 12px",
                      }}
                    >
                      {action}
                    </button>
                  ))}
                </div>
                {controls.error ? (
                  <p style={{ color: "#7b1f1f", marginTop: "12px" }}>{controls.error}</p>
                ) : null}
              </>
            ) : null}
            {panel.id === "chat-intervention-panel" ? (
              <>
                <p style={sectionTitleStyle}>Active Sessions</p>
                <ul style={listStyle}>
                  {(snapshot?.activeSessions ?? []).map((session) => (
                    <li key={session.sessionId} style={listItemStyle}>
                      {session.sessionId} · {session.status}
                    </li>
                  ))}
                </ul>
                <button
                  onClick={() => {
                    void sessionLifecycle.createOrResume();
                  }}
                  style={{
                    borderRadius: "999px",
                    border: "1px solid rgba(23, 33, 31, 0.18)",
                    background: "#fff7e8",
                    justifySelf: "start",
                    marginTop: "12px",
                    padding: "8px 12px",
                  }}
                >
                  {sessionLifecycle.submitting ? "syncing..." : "create / resume session"}
                </button>
                {sessionLifecycle.error ? (
                  <p style={{ color: "#7b1f1f", marginTop: "12px" }}>{sessionLifecycle.error}</p>
                ) : null}
                <p style={sectionTitleStyle}>Intervention Draft</p>
                <div style={{ display: "grid", gap: "8px" }}>
                  <textarea
                    disabled={!snapshot?.activeSessions[0]}
                    onChange={(event) => chat.setDraft(event.target.value)}
                    placeholder="Interrupt the current run with a human instruction..."
                    style={{
                      minHeight: "96px",
                      border: "1px solid rgba(23, 33, 31, 0.18)",
                      borderRadius: "12px",
                      font: "inherit",
                      padding: "10px 12px",
                      resize: "vertical",
                    }}
                    value={chat.draft}
                  />
                  <button
                    disabled={!snapshot?.activeSessions[0] || chat.submitting || !chat.draft.trim()}
                    onClick={() => {
                      void chat.submit();
                    }}
                    style={{
                      borderRadius: "999px",
                      border: "1px solid rgba(23, 33, 31, 0.18)",
                      background:
                        snapshot?.activeSessions[0] && chat.draft.trim() ? "#fff7e8" : "#efe9dc",
                      justifySelf: "start",
                      opacity:
                        snapshot?.activeSessions[0] && chat.draft.trim() && !chat.submitting
                          ? 1
                          : 0.55,
                      padding: "8px 12px",
                    }}
                  >
                    {chat.submitting ? "sending..." : "send intervention"}
                  </button>
                  {chat.error ? (
                    <p style={{ color: "#7b1f1f", marginTop: "4px" }}>{chat.error}</p>
                  ) : null}
                </div>
                <p style={sectionTitleStyle}>Recent Decisions</p>
                <ul style={listStyle}>
                  {recentDecisionEvents.length > 0 ? (
                    recentDecisionEvents.map((event) => (
                      <li key={event.eventId} style={listItemStyle}>
                        {event.type === "InputArbitrationRecorded"
                          ? `${event.type}: ${event.outcome} · ${event.details}`
                          : `${event.type}: ${event.decision}`}
                      </li>
                    ))
                  ) : (
                    <li style={listItemStyle}>No chat/governance events yet.</li>
                  )}
                </ul>
              </>
            ) : null}
            {panel.id === "agent-roster" ? (
              <ul style={listStyle}>
                {(snapshot?.activeAgents ?? []).map((agent) => (
                  <li key={agent.agentId} style={listItemStyle}>
                    <strong>{agent.agentId}</strong>
                    <div>{agent.phase}</div>
                    <div>{agent.lastAction}</div>
                    {agent.blocker ? <div>{`Blocker: ${agent.blocker}`}</div> : null}
                  </li>
                ))}
              </ul>
            ) : null}
            {panel.id === "embedded-terminal" ? (
              <>
                <p style={sectionTitleStyle}>Attachable Targets</p>
                <ul style={listStyle}>
                  {(snapshot?.terminalTargets ?? []).map((target) => (
                    <li key={target.terminalTarget} style={listItemStyle}>
                      <div>{target.terminalTarget} · {target.sessionId}</div>
                      <button
                        disabled={terminalAttach.submitting}
                        onClick={() => {
                          void terminalAttach.attach(target.terminalTarget);
                        }}
                        style={{
                          borderRadius: "999px",
                          border: "1px solid rgba(23, 33, 31, 0.18)",
                          background:
                            terminalAttach.attachedTarget === target.terminalTarget
                              ? "#d5e6df"
                              : "#fff7e8",
                          marginTop: "8px",
                          padding: "6px 10px",
                        }}
                      >
                        {terminalAttach.attachedTarget === target.terminalTarget
                          ? "attached"
                          : terminalAttach.submitting
                            ? "attaching..."
                            : "attach"}
                      </button>
                    </li>
                  ))}
                </ul>
                {terminalAttach.error ? (
                  <p style={{ color: "#7b1f1f", marginTop: "12px" }}>{terminalAttach.error}</p>
                ) : null}
                <p style={sectionTitleStyle}>Recent Stream</p>
                {terminalAttach.attachedTarget ? (
                  <p style={{ marginTop: 0 }}>
                    Attached target: <strong>{terminalAttach.attachedTarget}</strong>
                  </p>
                ) : null}
                <ul style={listStyle}>
                  {recentTerminalEvents.length > 0 ? (
                    recentTerminalEvents.map((event) => (
                      <li key={event.eventId} style={listItemStyle}>
                        <strong>{event.terminalTarget}</strong>
                        <div>{event.chunk}</div>
                      </li>
                    ))
                  ) : (
                    <li style={listItemStyle}>
                      {terminalAttach.attachedTarget
                        ? "No terminal stream events yet for the attached target."
                        : "Attach a terminal target to start observing stream output."}
                    </li>
                  )}
                </ul>
              </>
            ) : null}
          </article>
        ))}
      </section>
    </main>
  );
}
