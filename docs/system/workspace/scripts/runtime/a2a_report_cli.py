#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_protocol import ReportStore, DecisionStore

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd", required=True)
    r=sub.add_parser("record"); r.add_argument("--project",default="."); r.add_argument("--task-id",required=True); r.add_argument("--role",required=True); r.add_argument("--report-state",required=True); r.add_argument("--summary",required=True); r.add_argument("--next-action",default=""); r.add_argument("--attention-json",default="")
    l=sub.add_parser("list"); l.add_argument("--project",default="."); l.add_argument("--task-id",default=""); l.add_argument("--json",action="store_true")
    d=sub.add_parser("decide"); d.add_argument("--project",default="."); d.add_argument("--decisions-json",required=True)
    dl=sub.add_parser("decisions"); dl.add_argument("--project",default="."); dl.add_argument("--json",action="store_true")
    a=ap.parse_args(); db=Path(a.project)/".freely/freely.db"
    if a.cmd=="record":
        att=json.loads(a.attention_json) if a.attention_json else None
        print(json.dumps(ReportStore(db).record({"task_id":a.task_id,"role":a.role,"report_state":a.report_state,"summary":a.summary,"next_action":a.next_action,"attention":att}),ensure_ascii=False))
    elif a.cmd=="list":
        print(json.dumps({"reports":ReportStore(db).list(a.task_id or None)},ensure_ascii=False,indent=2) if a.json else ReportStore(db).list(a.task_id or None))
    elif a.cmd=="decide":
        store=DecisionStore(db); n=0
        for item in json.loads(a.decisions_json): n+=store.record(item["trigger_id"],item["decision"],item["reason"])
        print(json.dumps({"inserted":n}))
    else:
        print(json.dumps({"decisions":DecisionStore(db).list()},ensure_ascii=False,indent=2) if a.json else DecisionStore(db).list())
    return 0
if __name__=="__main__": raise SystemExit(main())
