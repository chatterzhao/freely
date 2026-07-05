# Pre-Tests: url-content-intake-skill-and-wechat-fetch-governance

## Acceptance Structure

### Pre-merge focused gate acceptance

- acceptance target: `url content intake skill materialization`
- testing layer: `focused skill regression`
- target environment: `feature worktree`
- required evidence: skill directory, bundled scripts, and targeted script test
- blocker taxonomy:
  - `definition_missing`
  - `skill_assets_missing`
  - `script_contract_missing`
  - `execution_pending_or_failed`

1. Skill bundle is self-contained
- setup:
  - inspect `docs/system/workspace/skills/url-content-intake/`
- expect:
  - skill root exists
  - bundled scripts live inside the skill directory
  - platform references exist alongside the skill

2. WeChat URL fetch uses browser-like headers
- setup:
  - run the focused skill test with fake curl injection
- expect:
  - `mp.weixin.qq.com/s/*` selects browser UA and common request headers

3. Generic URL fetch stays generic
- setup:
  - run the focused skill test against a non-WeChat HTTPS URL
- expect:
  - structured success fields are emitted
  - WeChat-specific headers are not forced onto generic URLs

4. Unsupported scheme reports structured failure
- setup:
  - run the script against a non-HTTP(S) URL
- expect:
  - script exits non-zero
  - `fetch_status`, `failure_reason`, and `recommended_next_step` stay structured

5. Readable extraction strips obvious noise
- setup:
  - feed sample WeChat HTML into the extractor
- expect:
  - readable text survives
  - obvious script noise does not survive

### Post-merge canonical truth acceptance

- acceptance target: `canonical develop carries the materialized url intake skill`
- testing layer: `develop truth replay`
- target environment: `develop`
- required evidence: verification artifact, progress closeout, and canonical test replay
- blocker taxonomy:
  - `definition_missing`
  - `evidence_plan_missing`
  - `execution_pending_or_failed`

1. Develop keeps the skill bundle and test together
- expect:
  - the skill remains shareable without depending on scattered repo-only helpers

2. Focused skill regression remains green on develop
- expect:
  - URL intake behavior stays stable after merge/writeback

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `url-content-intake skill directory includes bundled scripts and references`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/skills/url-content-intake/SKILL.md`

### PT-2
- id: `PT-2`
- requirement: `wechat article urls use browser-style headers by default`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-url-content-intake-skill`

### PT-3
- id: `PT-3`
- requirement: `generic urls keep generic fetch behavior and structured success fields`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-url-content-intake-skill`

### PT-4
- id: `PT-4`
- requirement: `unsupported schemes fail structurally instead of pretending success`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-url-content-intake-skill`

### PT-5
- id: `PT-5`
- requirement: `readable extraction preserves article text while dropping obvious script noise`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-url-content-intake-skill`

### PT-6
- id: `PT-6`
- requirement: `verification artifact records canonical develop replay and lifecycle closeout`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/human/url-content-intake-skill-and-wechat-fetch-governance/code-reviews/20260401-url-content-intake-skill-verification.md`
