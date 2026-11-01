#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_config import apply, validate

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("action", choices=["show","list","validate","apply"])
    ap.add_argument("--project", default=".")
    ap.add_argument("--role", default="")
    ap.add_argument("--slot", default="")
    ap.add_argument("--json", action="store_true")
    a=ap.parse_args()
    if a.action in {"validate","apply"}:
        if not a.role or not a.slot:
            print("--role and --slot required", file=sys.stderr); return 2
        r=apply(a.project,a.role,a.slot) if a.action=="apply" else validate(a.project,a.role,a.slot)
        print(json.dumps(r,ensure_ascii=False,indent=2) if a.json else ("ok" if r["ok"] else "fail: "+"; ".join(r["errors"])))
        return 0 if r["ok"] else 3
    # show/list delegate to harness-status for a single source of truth
    import subprocess
    cmd=[sys.executable,str(Path(__file__).resolve().parent/"harness_status.py"),"--project",a.project,"--json"]
    if a.role: cmd += ["--role",a.role]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print(r.stderr,file=sys.stderr); return r.returncode
    d=json.loads(r.stdout)
    print(json.dumps(d,ensure_ascii=False,indent=2) if a.json else "\n".join(f"{x['role']} {x['slot']} {x.get('satisfied')}" for x in d["roles"]))
    return 0
if __name__=="__main__": raise SystemExit(main())
