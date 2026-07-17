#!/bin/bash
# AT-002: __main__ 语义沙箱 — watchdog_run 阻塞点前 _get_agent_slot 必须已定义
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/watchdog_sse.py"
python3 - "$F" <<'PY'
import sys,ast,types
src=open(sys.argv[1]).read()
ns={'__name__':'__main__'}
class _Blocked(Exception): pass
def _stub(*a,**k): raise _Blocked()
tree=ast.parse(src)
try:
    for node in tree.body:
        if isinstance(node,ast.If) and getattr(getattr(node.test,'left',None),'id','')=='__name__':
            ns['watchdog_run']=_stub
            class _P:
                def add_argument(self,*a,**k): pass
                def parse_args(self): return types.SimpleNamespace(project='/tmp',a2a_socket='/tmp/x.sock')
            ns['argparse']=types.SimpleNamespace(ArgumentParser=lambda **k:_P())
        exec(compile(ast.Module([node],[]),'<node>','exec'),ns)
except _Blocked:
    pass
except SystemExit:
    pass
ok='_get_agent_slot' in ns
print(f"defined_before_block={ok}")
print("AT-002 PASS" if ok else "AT-002 FAIL: 阻塞点前未定义(死代码位置)")
PY
