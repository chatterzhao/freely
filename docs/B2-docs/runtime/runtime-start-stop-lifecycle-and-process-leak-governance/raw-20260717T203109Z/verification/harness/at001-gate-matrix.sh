#!/usr/bin/env bash
# AT-001: gate 三态矩阵均有可见 stderr 输出（gate 不再因 db 缺席静默杀死 wt-close）
# usage: at001-gate-matrix.sh <wtclose_script> <dev_worktree_dir>
set -uo pipefail
WTC="$1"; DW="$2"
MERGED_KEY=20260717T004620Z   # 已合并 lane（caa39491d, PR #3951）
FAKE_KEY=20260717T999998Z
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cd "$DW"
fail=0
run() { # name env_key target expect_substr
  local name="$1" envk="$2" target="$3" expect="$4"
  if [[ -n "$envk" ]]; then
    PROJECT_ROOT="$DW" FREELY_AGENT_RAW_KEY="$envk" bash "$WTC" --raw-key "$target" --dry-run 2>"$T/$name.log" >/dev/null
  else
    env -u FREELY_AGENT_RAW_KEY PROJECT_ROOT="$DW" bash "$WTC" --raw-key "$target" --dry-run 2>"$T/$name.log" >/dev/null
  fi
  local bytes; bytes=$(wc -c <"$T/$name.log" | tr -d ' ')
  if [[ "$bytes" -eq 0 ]]; then echo "  $name: FAIL (0 bytes stderr — silent death)"; fail=1; return; fi
  if ! grep -q "closeout-gate" "$T/$name.log"; then echo "  $name: FAIL (no [closeout-gate] line)"; fail=1; return; fi
  if ! grep -q "$expect" "$T/$name.log"; then echo "  $name: FAIL (missing: $expect)"; sed -n '1,3p' "$T/$name.log" | sed 's/^/    /'; fail=1; return; fi
  echo "  $name: ok ($(grep -m1 closeout-gate "$T/$name.log"))"
}
run g1-foreign-merged   ""           "$MERGED_KEY" "closeout-gate"
run g2-self-unfinished  "$FAKE_KEY"  "$FAKE_KEY"   "allowing close"
run g3-foreign-unfinish "20260717T999999Z" "$FAKE_KEY" "DENIED foreign unfinished"
[[ $fail -eq 0 ]] && echo "AT001_RESULT: PASS" || echo "AT001_RESULT: FAIL"
exit $fail
