# Brainstorm: supply-chain-baseline-and-install-intake-audit-governance

## Confirmed Boundary

This owner is the next narrow automation-first security slice after:

- execution-boundary review support
- build artifact exposure and release allowlist

It does not reopen those owners. It materializes only supply-chain and install-intake baseline truth that can be enforced locally today.

## Frozen Decisions

1. Root `package.json` implies a required root lockfile.
2. Direct dependency sources using `git+`, `github:`, `http(s):`, `file:`, or `link:` fail baseline.
3. Install-time lifecycle scripts `preinstall`, `install`, `postinstall`, and `prepare` fail baseline unless the script name is explicitly allowlisted in repo truth.
4. The lifecycle allowlist file exists even when it is empty, so exceptions stay machine-visible.
5. External GitHub Actions `uses:` refs must pin to full commit SHAs.
6. `freely doctor` replays the exact same audit instead of inventing a parallel rule set.
