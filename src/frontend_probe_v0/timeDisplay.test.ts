// @ts-nocheck
import { describe, expect, it } from "bun:test";

import { formatTimestampForDisplay, getSystemTimeZone } from "./timeDisplay";

describe("timeDisplay", () => {
  it("formats RFC3339 timestamps with the host system timezone", () => {
    const formatted = formatTimestampForDisplay("2026-04-02T18:30:00Z", "en-US");
    const expected = new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit",
      second: "2-digit",
      timeZoneName: "short",
    }).format(new Date("2026-04-02T18:30:00Z"));

    expect(getSystemTimeZone()).toBe(
      Intl.DateTimeFormat().resolvedOptions().timeZone || "system local time",
    );
    expect(formatted).toBe(expected);
  });

  it("returns the original value when the timestamp cannot be parsed", () => {
    expect(formatTimestampForDisplay("not-a-timestamp", "en-US")).toBe(
      "not-a-timestamp",
    );
  });
});
