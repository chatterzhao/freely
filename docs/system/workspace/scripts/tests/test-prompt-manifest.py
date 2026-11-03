#!/usr/bin/env python3
import importlib.util,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]; MOD=ROOT/'docs/system/workspace/scripts/runtime/prompt_manifest.py'
def load():
    if not MOD.exists(): raise AssertionError(f'missing module: {MOD}')
    spec=importlib.util.spec_from_file_location('prompt_manifest',MOD); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
NAMES=['agent_role','bootstrap','fleet','exit_contract','scan','chat','continuation','context_warning','checkpoint','thread_history','session_handoff']
def prompt(tail=''):
    return ''.join(f'<!-- FREELY_SEGMENT:{n} -->\n{n}{tail if n in {"scan","chat","session_handoff"} else ""}\n' for n in NAMES)
class T(unittest.TestCase):
    def test_prefix_stable(self):
        m=load(); a=m.build_manifest(prompt('A')); b=m.build_manifest(prompt('B'))
        self.assertEqual(len(a['segments']),11); self.assertEqual(a['prefix_hash'],b['prefix_hash']); self.assertNotEqual(a['segments'][-1]['sha256'],b['segments'][-1]['sha256'])
    def test_no_markers_full_prompt(self):
        m=load(); a=m.build_manifest('plain prompt')
        self.assertEqual([x['name'] for x in a['segments']],['full_prompt'])
    def test_usage_three_state(self):
        m=load(); self.assertEqual(m.hit_rate('reported',80,20),0.8); self.assertIsNone(m.hit_rate('estimated',0,0)); self.assertIsNone(m.hit_rate('absent',1,1))
if __name__=='__main__': unittest.main()
