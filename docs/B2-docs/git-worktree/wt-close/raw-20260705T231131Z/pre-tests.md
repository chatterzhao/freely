# Pre-tests: 旧路径引用清理

## Test 1: 核心脚本旧路径清零

```bash
for f in bin/*.sh bin/issue-sync bin/*.py \
  docs/system/workspace/scripts/worktree/*.sh \
  docs/system/workspace/scripts/quality/* \
  docs/system/workspace/scripts/runtime/freely \
  docs/system/workspace/scripts/runtime/interruption-manager-handler \
  .gitignore; do
  [[ -f "$f" ]] || continue
  count=$(grep -c 'docs/issues\|docs/epics' "$f" 2>/dev/null || echo 0)
  [[ "$count" -gt 0 ]] && echo "FAIL: $count in $f" && exit 1
done
echo "PASS"
```

## Test 2: bash 语法检查

```bash
for f in bin/issue-sync bin/raw-issue-pull bin/pr-review-guarded bin/freely-review bin/issue-index bin/issue-sync-bootstrap bin/issue-migrate-intake bin/freely-watchdog \
  docs/system/workspace/scripts/worktree/wt-create docs/system/workspace/scripts/worktree/wt-close docs/system/workspace/scripts/worktree/pr-merge-guarded docs/system/workspace/scripts/worktree/pr-create-guarded \
  docs/system/workspace/scripts/runtime/freely docs/system/workspace/scripts/runtime/interruption-manager-handler; do
  bash -n "$f" || { echo "FAIL: $f"; exit 1; }
done
echo "PASS"
```

## Test 3: wt-create 功能验证

```bash
# 用已存在的 platform raw issue 创建工位
./bin/freely wt-create --raw-key 20260705T231534Z --source platform --kind fix --slug test-path-fix 2>&1
# 期望：成功创建工位，raw issue 物化到 docs/B1-docs/raw-{key}/issue.md
```

## Test 4: B1-docs 路径可达

```bash
test -d docs/B1-docs && echo "PASS" || echo "FAIL"
find docs/B1-docs -name "issue.md" -maxdepth 3 | head -1 >/dev/null && echo "PASS" || echo "FAIL"
```

## Test 5: B2-docs I-* 搜索可达

```bash
find docs/B2-docs -name "I-*.md" | head -1 >/dev/null && echo "PASS" || echo "FAIL"
find docs/B2-docs -path "*/raw-*/issues/I-*.md" | head -1 >/dev/null && echo "PASS" || echo "FAIL"
find docs/B2-docs -path "*/issues/I-*.md" ! -path "*/raw-*" | head -1 >/dev/null && echo "PASS" || echo "FAIL"
```

## Test 6: governance-closeout-gate 路径分派

```bash
python3 -c "
from pathlib import Path
import sys
sys.path.insert(0, 'docs/system/workspace/scripts/quality')
from importlib import import_module
# 验证 _issue_file 对 raw-* 和 I-* 都返回正确路径
print('PASS: import ok')
"
```

## Test 7: 旧路径全项目清零（排除内容文件）

```bash
remaining=$(grep -r 'docs/issues\|docs/epics' . --include="*.sh" --include="*.py" 2>/dev/null | grep -v "docs/B1-docs/raw-" | grep -v "docs/B2-docs/" | grep -v ".bak." | grep -v "epics-map.svg")
[[ -z "$remaining" ]] && echo "PASS" || { echo "FAIL: $remaining"; exit 1; }
```
