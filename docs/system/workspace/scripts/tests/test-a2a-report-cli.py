#!/usr/bin/env python3
import json,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]; CLI=ROOT/'bin/a2a-report'
class T(unittest.TestCase):
    def test_record_list(self):
        self.assertTrue(CLI.exists(),f'missing CLI: {CLI}')
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp); (p/'.freely').mkdir()
            att=json.dumps({'needed':True,'question':'q','target_role':'manager'})
            r=subprocess.run([str(CLI),'record','--project',str(p),'--task-id','T','--role','worker','--report-state','ready','--summary','s','--attention-json',att],capture_output=True,text=True); self.assertEqual(r.returncode,0,r.stderr)
            r=subprocess.run([str(CLI),'list','--project',str(p),'--task-id','T','--json'],capture_output=True,text=True); self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(r.stdout)['reports'][0]['report_state'],'ready')
if __name__=='__main__': unittest.main()
