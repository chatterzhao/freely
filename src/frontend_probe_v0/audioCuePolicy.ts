import type { AudioCueKey, ServerEvent } from "./contracts";

export function getAudioCueKey(event: ServerEvent): AudioCueKey | null {
  if (event.type !== "AudioCueRequested") {
    return null;
  }

  return event.cueKey;
}
