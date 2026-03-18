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
  constructor(
    private readonly invoke: TauriInvoke,
    private readonly listen: TauriListen,
    private readonly bindings: ProbeBridgeBindings = defaultProbeBridgeBindings,
  ) {}

  requestSnapshot(projectId: string): Promise<ProbeSnapshot> {
    return this.invoke<ProbeSnapshot>(this.bindings.requestSnapshotCommand, {
      projectId,
    });
  }

  sendCommand(command: ClientCommand): Promise<void> {
    return this.invoke<void>(this.bindings.sendCommandCommand, {
      command,
    });
  }

  subscribe(listener: EventListener): () => void {
    let disposed = false;
    let unlisten: (() => void) | null = null;

    void this.listen(this.bindings.serverEventName, (event) => {
      listener(event.payload);
    }).then((cleanup) => {
      if (disposed) {
        cleanup();
        return;
      }

      unlisten = cleanup;
    });

    return () => {
      disposed = true;
      unlisten?.();
    };
  }
}
