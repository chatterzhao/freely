import type { ServerEvent } from "./contracts";
import { invoke, isTauri } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";

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
  const resolvedInvoke = runtime?.invoke ?? runtime?.core?.invoke;
  const resolvedListen = runtime?.listen ?? runtime?.event?.listen;

  if (resolvedInvoke && resolvedListen) {
    return {
      invoke: resolvedInvoke,
      listen: resolvedListen,
    };
  }

  if (!isTauri()) {
    return null;
  }

  return {
    invoke,
    listen: async (eventName, listener) =>
      listen<ServerEvent>(eventName, (event) =>
        listener({ payload: event.payload }),
      ),
  };
}
