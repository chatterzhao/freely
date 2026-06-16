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
  mkdir -p "$dir/docs/pre-brainstorms/20260309-0000--sample"
  cp "$ROOT_DIR/docs/PROJECT_INTENT.md" "$dir/docs/PROJECT_INTENT.md"
  cp "$ROOT_DIR/docs/CONSTITUTION.md" "$dir/docs/CONSTITUTION.md"
  cp "$ROOT_DIR/docs/LAWS.md" "$dir/docs/LAWS.md"
  cp "$ROOT_DIR/AGENTS.md" "$dir/AGENTS.md"
  cp "$ROOT_DIR/docs/pre-brainstorms/README.md" "$dir/docs/pre-brainstorms/README.md"
  cp "$ROOT_DIR/docs/pre-brainstorms/INDEX.md" "$dir/docs/pre-brainstorms/INDEX.md"
  cp "$ROOT_DIR/docs/pre-brainstorms/CONVERGENCE.md" "$dir/docs/pre-brainstorms/CONVERGENCE.md"
  cp "$ROOT_DIR/docs/pre-brainstorms/20260309-2345--governance-check-naming-alignment/brainstorms.md" \
    "$dir/docs/pre-brainstorms/20260309-0000--sample/brainstorms.md"
  cp "$ROOT_DIR/docs/pre-brainstorms/20260309-2345--governance-check-naming-alignment/candidates.md" \
    "$dir/docs/pre-brainstorms/20260309-0000--sample/candidates.md"
  cat > "$dir/docs/pre-brainstorms/INDEX.md" <<'EOT'
# Pre-brainstorm 索引（IBM Framework B1）

## 条目
- 20260309-0000--sample
  - brainstorms: docs/pre-brainstorms/20260309-0000--sample/brainstorms.md
  - candidates: docs/pre-brainstorms/20260309-0000--sample/candidates.md
EOT
  echo "$dir"
}

# CASE-001: pre-brainstorms 缺失时 doctor 失败
p1="$(new_project)"
rm -rf "$p1/docs/pre-brainstorms"
expect_fail "CASE-001 doctor fails when pre-brainstorms missing" "$FREELY" doctor --project "$p1"

# CASE-002: 缺失 AGENTS 时 doctor 失败
p2="$(new_project)"
rm -f "$p2/AGENTS.md"
expect_fail "CASE-002 doctor fails when AGENTS missing" "$FREELY" doctor --project "$p2"

# CASE-003 + CASE-006: 治理文档齐备时 doctor 成功并返回 0
p3="$(new_project)"
expect_pass "CASE-003 doctor passes with active governance docs" "$FREELY" doctor --project "$p3"

# CASE-004: start 在门禁失败时阻断
p4="$(new_project)"
expect_pass "prepare config via init" "$FREELY" init --project "$p4" --intent "$p4/docs/PROJECT_INTENT.md" --constitution "$p4/docs/CONSTITUTION.md" --ai codex:gpt-5-codex:auto
rm -f "$p4/docs/LAWS.md"
expect_fail "CASE-004 start blocked before launching loop" "$FREELY" start --project "$p4"

# CASE-004B: init 可显式写入 reasoning effort 配置
p4b="$(new_project)"
expect_pass "CASE-004B init accepts reasoning effort" "$FREELY" init --project "$p4b" --intent "$p4b/docs/PROJECT_INTENT.md" --constitution "$p4b/docs/CONSTITUTION.md" --ai codex:gpt-5.4:auto --reasoning-effort medium
grep -q 'AI_REASONING_EFFORT = "medium"' "$p4b/.freely/config.toml" || fail "CASE-004B expected reasoning effort in config"
pass "CASE-004B reasoning effort persisted in config"

# CASE-005: doctor 失败输出具体缺失文档路径（用 stderr 文本验证）
p5="$(new_project)"
rm -f "$p5/docs/LAWS.md"
if "$FREELY" doctor --project "$p5" >/tmp/freely-doctor-out.txt 2>/tmp/freely-doctor-err.txt; then
  fail "CASE-005 expected doctor failure for missing LAWS"
fi
if ! grep -q "$p5/docs/LAWS.md" /tmp/freely-doctor-err.txt; then
  fail "CASE-005 expected missing path in doctor stderr"
fi
pass "CASE-005 doctor error includes missing file path"

echo "All doc gate tests passed."
