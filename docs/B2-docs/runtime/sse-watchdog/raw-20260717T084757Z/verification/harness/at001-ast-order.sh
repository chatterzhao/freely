#!/bin/bash
# AT-001: main 块后无被引用 def + 日志带时间戳
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/watchdog_sse.py"
python3 - "$F" <<'PY'
import ast,sys
src=open(sys.argv[1]).read()
tree=ast.parse(src)
main_idx=None
for i,node in enumerate(tree.body):
    if isinstance(node,ast.If) and getattr(getattr(node.test,'left',None),'id','')=='__name__':
        main_idx=i
after=[n.name for n in tree.body[main_idx+1:] if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))] if main_idx is not None else []
referenced=[n for n in after if src.count(n+'(')>1]
ts=('def _log(' in src) or ('strftime' in src)
print(f"defs_after_main={after} referenced_dead={referenced} timestamped={ts}")
if not referenced and ts: print("AT-001 PASS")
else: print("AT-001 FAIL")
PY
