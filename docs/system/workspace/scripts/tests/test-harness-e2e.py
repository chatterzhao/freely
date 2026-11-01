#!/usr/bin/env python3
import json,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]
CLI=ROOT/'bin/harness-select'
class T(unittest.TestCase):
    def test_cli_chain(self):
        self.assertTrue(CLI.exists(),f'missing CLI: {CLI}')
        with tempfile.TemporaryDirectory() as tmp:
            p=pathlib.Path(tmp); (p/'.freely').mkdir()
            (p/'.freely/config.toml').write_text('AGENT_AI_TOOL_ADAPTER = "acp"\nFREELY_ACP_CLINE_BIN = "/usr/bin/true"\n')
            (p/'.freely/agent-table.toml').write_text('[[agents]]\nrole="reviewer"\nreviewer_id="reviewer_01"\nreviewer_slot="cline-account-x"\npool=9\n')
            r=subprocess.run([str(CLI),'show','--project',str(p),'--json'],capture_output=True,text=True); self.assertEqual(r.returncode,0,r.stderr)
            r=subprocess.run([str(CLI),'apply','--project',str(p),'--role','reviewer','--slot','cline-account-y'],capture_output=True,text=True); self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('cline-account-y',(p/'.freely/agent-table.toml').read_text())
if __name__=='__main__': unittest.main()
