#!/usr/bin/env python3
import importlib.util,pathlib,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]; MOD=ROOT/'docs/system/workspace/scripts/runtime/prompt_manifest.py'
def load():
    if not MOD.exists(): raise AssertionError(f'missing module: {MOD}')
    spec=importlib.util.spec_from_file_location('prompt_manifest',MOD); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
class T(unittest.TestCase):
    def test_record_jsonl(self):
        m=load()
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp); (p/'.freely/run').mkdir(parents=True)
            r=m.record_manifest(p,'<!-- FREELY_SEGMENT:agent_role -->\nrole\n<!-- FREELY_SEGMENT:bootstrap -->\nbody',role='manager',session_id='s1')
            self.assertTrue(r['recorded']); self.assertTrue((p/'.freely/run/prompt-manifest.jsonl').read_text().strip())
            src=(ROOT/'docs/system/workspace/scripts/runtime/run-acp-prompt.py').read_text()
            self.assertIn('record_manifest',src)
            self.assertIn('FREELY_SEGMENT:bootstrap',(ROOT/'docs/system/workspace/scripts/start-lead-agent.sh').read_text())
if __name__=='__main__': unittest.main()
