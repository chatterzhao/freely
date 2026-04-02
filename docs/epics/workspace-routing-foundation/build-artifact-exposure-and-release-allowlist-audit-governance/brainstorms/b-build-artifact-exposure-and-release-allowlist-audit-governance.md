# Brainstorms: build-artifact-exposure-and-release-allowlist-audit-governance

This owner materializes the smallest practical security capability slice that directly replaces manual release-output review:

1. scan build output for forbidden artifacts,
2. require an explicit allowlist for shipped files,
3. fail in `doctor` and build scripts when output drifts, and
4. keep production sourcemap posture explicit instead of implicit.

The slice stays narrow on purpose. Broader supply-chain, full secret scanning, and remediation automation remain follow-on owners.
