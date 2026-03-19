import type { ServerEvent } from "./contracts";

export type TauriInvoke = <T>(
  command: string,
  payload?: Record<string, unknown>,
) => Promise<T>;

export type TauriListen = (
  eventName: string,
  listener: (event: { payload: ServerEvent }) => void,
) => Promise<() => void>;

export type TauriRuntime = {
  invoke: TauriInvoke;
  listen: TauriListen;
};

type TauriGlobalLike = {
  invoke?: TauriInvoke;
  listen?: TauriListen;
  core?: {
    invoke?: TauriInvoke;
  };
  event?: {
    listen?: TauriListen;
  };
};

export function resolveTauriRuntime(runtime?: TauriGlobalLike): TauriRuntime | null {
  const invoke = runtime?.invoke ?? runtime?.core?.invoke;
  const listen = runtime?.listen ?? runtime?.event?.listen;

  if (!invoke || !listen) {
    return null;
  }

  return {
    invoke,
    listen,
  };
}
