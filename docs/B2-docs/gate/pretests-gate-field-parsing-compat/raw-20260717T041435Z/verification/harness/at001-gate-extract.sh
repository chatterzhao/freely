#!/usr/bin/env bash
# AT-001: pretests-gate 的 extract 对四种引号格式均解析出过 RE 的纯路径
set -u
GATE="$(pwd)/docs/system/workspace/scripts/quality/pretests-gate"
python3 - "$GATE" <<'PY'
import re,sys
src=open(sys.argv[1]).read()
m=re.search(r'def extract\(field: str\) -> str:\n(.*?)\n\n',src,re.DOTALL)
extract_src=m.group(0) if m else ''
# 取 extract 内的正则字面量
rm=re.search(r're\.search\(rf"(.+?)", text',extract_src)
if not rm:
    print("AT-001 FAIL: 无法定位 extract 正则"); sys.exit(0)
pat=rm.group(1)
path='docs/B2-docs/gate/x/raw-20260717T000000Z/code-reviews'
VR=re.compile(r"^docs/B2-docs/.+/raw-[^/]+/code-reviews$")
ok=0; total=4
for label,val in [("bare",path),("single",f"'{path}'"),("double",f'"{path}"'),("backtick",f"`{path}`")]:
    text=f"- verification_artifact_dir: {val}\n"
    p=pat.replace('{re.escape(field)}','verification_artifact_dir')
    mm=re.search(p,text,re.MULTILINE)
    got=mm.group(1).strip() if mm else ''
    if VR.match(got): ok+=1
    else: print(f"{label} 解析失败: got={got!r}")
print(f"AT-001 {'PASS' if ok==total else 'FAIL'}: {ok}/{total} 格式解析通过" if ok==total else f"AT-001 FAIL: quoted 格式解析失败 ({ok}/{total})")
PY
