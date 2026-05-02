import { createElement } from "react";

import { createDefaultProbeApp } from "./entry";

type RenderFn = (node: unknown) => void;

type MountOptions = {
  projectId?: string;
  transportMode?: "mock" | "tauri-mock" | "tauri-broken";
  validationMode?: "off" | "tauri-smoke";
};

export function mountProbeApp(render: RenderFn, options?: MountOptions) {
  const { AppShell } = createDefaultProbeApp(options);
  render(createElement(AppShell));
}
