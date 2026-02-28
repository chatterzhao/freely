# Project Intent Template

## Project Name
<name>

## Core Intent
<one paragraph: what autonomous outcome this project should continuously pursue>

## Autonomous Behavior
- AI is the project owner once loop starts.
- AI self-manages: brainstorm -> EPIC -> STORY -> implementation -> verification.
- AI keeps iterating until stop criteria are met.

## Constitution Contract
- Constitution is mandatory hard constraint.
- Constitution should include (in this priority order):
  - branch/worktree policy
  - baseline project structure policy (docs, README.md, src, .env, .env.example or equivalent)
  - tech stack constraints
  - BMAD document discipline (BMA execution workflow)
  - external system and integration constraints

## Recovery Contract
- Resume-first when unattended resume is supported.
- If unattended resume is not supported:
  1. run bridge recovery to write crash/blocking checkpoint into progress docs
  2. restart unattended execution from updated project state

## Input Surface
- project absolute path
- intent file path
- constitution file path
- ai spec `tool:model:mode`

## Stop Criteria
<explicit termination rules; if empty, loop is continuous by default>
