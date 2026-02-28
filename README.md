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

./bin/freely start --project /home/devbox/project/my-fasterp4/fasterp4
```

In another terminal:

```bash
./bin/freely status --project /home/devbox/project/my-fasterp4/fasterp4
./bin/freely stop --project /home/devbox/project/my-fasterp4/fasterp4
```
