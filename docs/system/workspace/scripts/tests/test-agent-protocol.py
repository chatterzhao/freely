#!/usr/bin/env python3
import importlib.util,pathlib,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]; MOD=ROOT/'docs/system/workspace/scripts/runtime/agent_protocol.py'
def load():
    if not MOD.exists(): raise AssertionError(f'missing module: {MOD}')
    spec=importlib.util.spec_from_file_location('agent_protocol',MOD); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
class T(unittest.TestCase):
    def test_report_six_states(self):
        m=load()
        for st in ['progress','waiting','ready','blocked','failed','dropped']:
            r=m.validate_report({'task_id':'T','role':'worker','report_state':st,'summary':'s'})
            self.assertTrue(r['ok'],r)
        self.assertFalse(m.validate_report({'task_id':'T','role':'worker','report_state':'nope','summary':'s'})['ok'])
        self.assertFalse(m.validate_report({'task_id':'T','role':'worker','report_state':'ready','summary':''})['ok'])
    def test_attention_single_question(self):
        m=load()
        a=m.validate_attention({'needed':True,'question':'q','target_role':'manager'})
        self.assertTrue(a['ok'],a)
        self.assertFalse(m.validate_attention({'needed':True,'question':'q','target_role':'manager','human_action':'a','for_trigger_id':'e','extra':'x'})['ok'])
        self.assertFalse(m.validate_attention({'needed':True,'question':'q'})['ok'])
        self.assertTrue(m.validate_attention({'needed':False})['ok'])
    def test_report_store(self):
        m=load()
        with tempfile.TemporaryDirectory() as tmp:
            s=m.ReportStore(pathlib.Path(tmp)/'a.db')
            s.record({'task_id':'T','role':'worker','report_state':'ready','summary':'s'})
            self.assertEqual(len(s.list('T')),1)
    def test_decision_idempotent(self):
        m=load()
        with tempfile.TemporaryDirectory() as tmp:
            s=m.DecisionStore(pathlib.Path(tmp)/'a.db')
            self.assertEqual(s.record('e1','accept','explicit'),1)
            self.assertEqual(s.record('e1','ignore','dup'),0)
            self.assertEqual(len(s.list()),1)
            with self.assertRaises(ValueError): s.record('e2','accept','')
if __name__=='__main__': unittest.main()
