#!/usr/bin/env python3
import json,pathlib,subprocess,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]
SCRIPT=ROOT/'docs/system/workspace/scripts/runtime/harness_status.py'
class T(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.p=pathlib.Path(self.tmp.name); (self.p/'.freely').mkdir()
        (self.p/'.freely/config.toml').write_text('AGENT_AI_TOOL_ADAPTER = "acp"\nFREELY_ACP_CLINE_BIN = "/usr/bin/true"\nFREELY_ACP_CLAUDE_BIN = "/usr/bin/true"\n')
        (self.p/'.freely/agent-table.toml').write_text('''[[agents]]\nrole="manager"\nmanager_id="manager_01"\nmanager_slot="claude-apikey-x"\npool=1\n\n[[agents]]\nrole="reviewer"\nreviewer_id="reviewer_01"\nreviewer_slot="cline-account-x"\npool=9\n''')
    def tearDown(self): self.tmp.cleanup()
    def run_cli(self, *a):
        return subprocess.run([sys.executable,str(SCRIPT),'--project',str(self.p),*a],capture_output=True,text=True)
    def test_role_filter_and_degraded(self):
        r=self.run_cli('--role','reviewer','--json'); self.assertEqual(r.returncode,0,r.stderr)
        d=json.loads(r.stdout); self.assertEqual([x['role'] for x in d['roles']],['reviewer'])
        role=d['roles'][0]; self.assertEqual(role['capabilities']['fork'],'degraded')
        self.assertTrue(role['satisfied']); self.assertIn('fork',role['degraded'])
    def test_unknown_role(self):
        r=self.run_cli('--role','nope','--json'); self.assertEqual(r.returncode,2)
if __name__=='__main__': unittest.main()
