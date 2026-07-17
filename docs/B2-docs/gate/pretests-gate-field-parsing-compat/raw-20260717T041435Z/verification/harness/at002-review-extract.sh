#!/usr/bin/env bash
# AT-002: pr-review-guarded 的取值逻辑对四种格式均得纯路径
set -u
RV="$(pwd)/bin/pr-review-guarded"
SEDLINE=$(grep -n "verification_artifact_dir:" "$RV" | grep "sed" | head -1 | cut -d: -f1)
[ -z "$SEDLINE" ] && { echo "AT-002 FAIL: 未找到取值行"; exit 0; }
EXPR=$(sed -n "${SEDLINE}p" "$RV")
path='docs/B2-docs/gate/x/raw-20260717T000000Z/code-reviews'
ok=0
for label in bare single double backtick; do
  case $label in
    bare) line="- verification_artifact_dir: $path" ;;
    single) line="- verification_artifact_dir: '$path'" ;;
    double) line="- verification_artifact_dir: \"$path\"" ;;
    backtick) line="- verification_artifact_dir: \`$path\`" ;;
  esac
  TMP=$(mktemp); printf '%s\n' "$line" > "$TMP"
  # 用与 pr-review-guarded 同一行逻辑取值（把 $_i_issue_file 替换为 TMP 执行）
  GOT=$(eval "$(printf '%s' "$EXPR" | sed 's/^[0-9]*://; s/_verification_dir=\$(//; s/ || true)$//; s|"\$_i_issue_file"|"'$TMP'"|')" 2>/dev/null | head -1)
  rm -f "$TMP"
  if [ "$GOT" = "$path" ]; then ok=$((ok+1)); else echo "$label 解析失败: got=$GOT"; fi
done
[ "$ok" -eq 4 ] && echo "AT-002 PASS: 4/4 格式解析通过" || echo "AT-002 FAIL: 裸值格式解析出整行 ($ok/4)"
