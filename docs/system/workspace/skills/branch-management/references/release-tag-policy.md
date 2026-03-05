# Release and Tag Policy

## Stage Format
- Tag format must be: `YYYY.MM.DD-HHMM-stage`
- `stage` is required and cannot be omitted.

## Stage by Branch
- `feature/*` -> `alpha` (local lightweight tag, do not push)
- `pre-develop` -> `beta` (local lightweight tag, do not push)
- `develop` -> `nightly` (push tag)
- `main` -> `stable` (push tag)
- `hotfix/*` -> `hotfix` (push tag)

## Release Branch Flow
1. Create `release/*` from `develop`.
2. Freeze and validate release content.
3. Merge `release/*` into `main`.
4. Back-merge release result into `develop`.

## Hotfix Flow
1. Create `hotfix/*` from `main`.
2. Merge hotfix into `main` and `develop`.
3. Sync hotfix result into `pre-develop`.

## Guardrails
- Never push `alpha`/`beta`.
- If required tests or governance checks fail, block release and block push tag.
