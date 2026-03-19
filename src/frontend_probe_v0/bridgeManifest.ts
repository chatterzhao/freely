import { defaultProbeBridgeBindings } from "./bridgeBindings";

export const probeBridgeManifest = {
  contractVersion: "freely.probe.v1",
  commands: {
    requestSnapshot: {
      commandName: defaultProbeBridgeBindings.requestSnapshotCommand,
      payloadShape: "{ projectId: string }",
    },
    sendCommand: {
      commandName: defaultProbeBridgeBindings.sendCommandCommand,
      payloadShape: "{ command: ClientCommand }",
    },
  },
  events: {
    serverEvent: {
      eventName: defaultProbeBridgeBindings.serverEventName,
      payloadShape: "ServerEvent",
    },
  },
} as const;
