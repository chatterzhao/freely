import type { ClientCommand, ProbeSnapshot, ServerEvent } from "./contracts";
import type { ProbeAdapter } from "./adapter";
import {
  defaultProbeBridgeBindings,
  type ProbeBridgeBindings,
} from "./bridgeBindings";
import type { EventListener } from "./events";

type TauriInvoke = <T>(command: string, payload?: Record<string, unknown>) => Promise<T>;
type TauriListen = (
  eventName: string,
  listener: (event: { payload: ServerEvent }) => void,
) => Promise<() => void>;

export class TauriProbeAdapter implements ProbeAdapter {
  private readonly listeners = new Set<EventListener>();
  private unlisten: (() => void) | null = null;
  private readonly listenerReady: Promise<void>;

  constructor(
    private readonly invoke: TauriInvoke,
    private readonly listen: TauriListen,
    private readonly bindings: ProbeBridgeBindings = defaultProbeBridgeBindings,
  ) {
    this.listenerReady = this.listen(this.bindings.serverEventName, (event) => {
      this.listeners.forEach((listener) => {
        listener(event.payload);
      });
    }).then((cleanup) => {
      this.unlisten = cleanup;
    });
  }

  async listProjects(): Promise<string[]> {
    try {
      // Backend-driven project discovery (Tauri command).
      return await this.invoke<string[]>("list_projects", {});
    } catch {
      // Fallback for backends without the list_projects command yet.
      return ["freely", "freely-sandbox", "frontend-probe-demo"];
    }
  }

  async requestSnapshot(projectId: string): Promise<ProbeSnapshot> {
    return this.invoke<ProbeSnapshot>(this.bindings.requestSnapshotCommand, {
      payload: {
        projectId,
      },
    });
  }

  sendCommand(command: ClientCommand): Promise<void> {
    return this.invoke<void>(this.bindings.sendCommandCommand, {
      command,
    });
  }

  subscribe(listener: EventListener): () => void {
    this.listeners.add(listener);

    return () => {
      this.listeners.delete(listener);
    };
  }
}
