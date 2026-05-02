import { useEffect, useRef, useState } from "react";

import type { ProbeAdapter } from "./adapter";
import { audioCueCatalog } from "./audioCueCatalog";
import { isEventCapableAdapter } from "./events";
import { getAudioCueKey } from "./audioCuePolicy";

type AudioState = {
  status: "idle" | "ready" | "playing" | "blocked";
  lastCueKey?: keyof typeof audioCueCatalog;
  lastError?: string;
};

function createAudioElement(url: string) {
  return new Audio(url);
}

export function useAudioNotifier(adapter: ProbeAdapter): AudioState {
  const playedEventIds = useRef(new Set<string>());
  const audioCache = useRef(new Map<string, HTMLAudioElement>());
  const [state, setState] = useState<AudioState>({ status: "idle" });

  useEffect(() => {
    if (!isEventCapableAdapter(adapter)) {
      return;
    }

    setState((current) => ({ ...current, status: "ready" }));

    return adapter.subscribe((event) => {
      const cueKey = getAudioCueKey(event);
      if (!cueKey || playedEventIds.current.has(event.eventId)) {
        return;
      }

      playedEventIds.current.add(event.eventId);
      const cue = audioCueCatalog[cueKey];
      const audio =
        audioCache.current.get(cue.url) ?? createAudioElement(cue.url);
      audioCache.current.set(cue.url, audio);
      audio.currentTime = 0;

      void audio.play().then(
        () => {
          setState({
            status: "playing",
            lastCueKey: cueKey,
          });
        },
        (cause) => {
          setState({
            status: "blocked",
            lastCueKey: cueKey,
            lastError: cause instanceof Error ? cause.message : String(cause),
          });
        },
      );
    });
  }, [adapter]);

  return state;
}
