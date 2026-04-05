import managerCompletedUrl from "./audio/manager-completed.wav";
import managerStartedUrl from "./audio/manager-started.wav";
import workerCompletedUrl from "./audio/worker-completed.wav";
import workerStartedUrl from "./audio/worker-started.wav";
import type { AudioCueKey } from "./contracts";

export type AudioCueDefinition = {
  cueKey: AudioCueKey;
  label: string;
  url: string;
};

export const audioCueCatalog: Record<AudioCueKey, AudioCueDefinition> = {
  "manager-started": {
    cueKey: "manager-started",
    label: "Manager Started",
    url: managerStartedUrl,
  },
  "manager-completed": {
    cueKey: "manager-completed",
    label: "Manager Completed",
    url: managerCompletedUrl,
  },
  "worker-started": {
    cueKey: "worker-started",
    label: "Worker Started",
    url: workerStartedUrl,
  },
  "worker-completed": {
    cueKey: "worker-completed",
    label: "Worker Completed",
    url: workerCompletedUrl,
  },
};
