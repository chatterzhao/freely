# freely

## Project Intent

Freely is an autonomous project loop runner:
- AI runs as the active worker for one project path.
- AI follows project intent + constitution as hard constraints.
- AI keeps continuity with monitor/restart behavior.

Primary docs:
- Project intent: `docs/PROJECT_INTENT.md`
- Constitution: `docs/CONSTITUTION.md`
- Documentation map: `docs/README.md`

## Quick Start

```bash
cd /home/devbox/project/freely
chmod +x ./bin/freely

./bin/freely init \
  --project /home/devbox/project/my-fasterp4/fasterp4 \
  --intent /home/devbox/project/freely/docs/PROJECT_INTENT.md \
  --constitution /home/devbox/project/freely/docs/CONSTITUTION.md \
  --ai codex:gpt-5-codex:auto

./bin/freely doctor --project /home/devbox/project/my-fasterp4/fasterp4
./bin/freely start --project /home/devbox/project/my-fasterp4/fasterp4
```

In another terminal:

```bash
./bin/freely status --project /home/devbox/project/my-fasterp4/fasterp4
./bin/freely stop --project /home/devbox/project/my-fasterp4/fasterp4
```

## BMAD Documentation Gate

Run BMAD baseline checks before implementation or merge:

```bash
chmod +x ./bin/bmad-check
./bin/bmad-check
```

## Hook Regression Gate

Validate local push policy before merge:

```bash
chmod +x ./bin/test-pre-push-hook
./bin/test-pre-push-hook
```

Branch policy for feature delivery:

- `feature/* -> pre-develop` for test integration
- `pre-develop -> develop` only after validation
- direct push/merge to `develop` is blocked by local hook policy
