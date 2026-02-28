#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
FREELY="$ROOT_DIR/bin/freely"

pass() { echo "[PASS] $*"; }
fail() { echo "[FAIL] $*" >&2; exit 1; }
expect_fail() {
  local desc="$1"
  shift
  if "$@"; then
    fail "$desc (expected failure, got success)"
  fi
  pass "$desc"
}
expect_pass() {
  local desc="$1"
  shift
  "$@" || fail "$desc"
  pass "$desc"
}

new_project() {
  local dir
  dir="$(mktemp -d)"
  mkdir -p "$dir/docs/brainstorm"
  cp "$ROOT_DIR/docs/PROJECT_INTENT.md" "$dir/docs/PROJECT_INTENT.md"
  cp "$ROOT_DIR/docs/CONSTITUTION.md" "$dir/docs/CONSTITUTION.md"
  cp "$ROOT_DIR/docs/brainstorm/BRAINSTORM.md" "$dir/docs/brainstorm/BRAINSTORM.md"
  cp "$ROOT_DIR/docs/PRD.md" "$dir/docs/PRD.md"
  cp "$ROOT_DIR/docs/EPIC.md" "$dir/docs/EPIC.md"
  cp "$ROOT_DIR/docs/STORY.md" "$dir/docs/STORY.md"
  cp "$ROOT_DIR/docs/PROGRESS.md" "$dir/docs/PROGRESS.md"
  cp "$ROOT_DIR/docs/RECOVERY.md" "$dir/docs/RECOVERY.md"
  echo "$dir"
}

# CASE-001: PRE_TEST 缺失
p1="$(new_project)"
expect_fail "CASE-001 doctor fails when PRE_TEST missing" "$FREELY" doctor --project "$p1"

# CASE-002: PRE_TEST 存在但没有 CASE-
p2="$(new_project)"
cat > "$p2/docs/PRE_TEST.md" <<'EOT'
# PRE_TEST
仅有说明，没有结构化用例。
EOT
expect_fail "CASE-002 doctor fails when PRE_TEST has no CASE" "$FREELY" doctor --project "$p2"

# CASE-003 + CASE-006: PRE_TEST 合法时 doctor 成功并返回 0
p3="$(new_project)"
cat > "$p3/docs/PRE_TEST.md" <<'EOT'
# PRE_TEST
- CASE-001: sample
EOT
expect_pass "CASE-003 doctor passes with CASE in PRE_TEST" "$FREELY" doctor --project "$p3"

# CASE-004: start 在门禁失败时阻断
p4="$(new_project)"
expect_pass "prepare config via init" "$FREELY" init --project "$p4" --intent "$p4/docs/PROJECT_INTENT.md" --constitution "$p4/docs/CONSTITUTION.md" --ai codex:gpt-5-codex:auto
expect_fail "CASE-004 start blocked before launching loop" "$FREELY" start --project "$p4"

# CASE-005: doctor 失败输出具体缺失文档路径（用 stderr 文本验证）
p5="$(new_project)"
rm -f "$p5/docs/EPIC.md"
if "$FREELY" doctor --project "$p5" >/tmp/freely-doctor-out.txt 2>/tmp/freely-doctor-err.txt; then
  fail "CASE-005 expected doctor failure for missing EPIC"
fi
if ! grep -q "$p5/docs/EPIC.md" /tmp/freely-doctor-err.txt; then
  fail "CASE-005 expected missing path in doctor stderr"
fi
pass "CASE-005 doctor error includes missing file path"

echo "All doc gate tests passed."
