#!/usr/bin/env python3
import importlib.util, pathlib, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[5]
MOD=ROOT/'docs/system/workspace/scripts/runtime/harness_config.py'
def load():
    if not MOD.exists(): raise AssertionError(f'missing module: {MOD}')
    spec=importlib.util.spec_from_file_location('harness_config',MOD); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
class T(unittest.TestCase):
    def setUp(self):
        self.m=load(); self.tmp=tempfile.TemporaryDirectory(); self.p=pathlib.Path(self.tmp.name)
        (self.p/'.freely').mkdir()
        (self.p/'.freely/config.toml').write_text('AGENT_AI_TOOL_ADAPTER = "acp"\nFREELY_ACP_CLAUDE_BIN = "/usr/bin/true"\nFREELY_ACP_CLINE_BIN = "/usr/bin/true"\n')
        (self.p/'.freely/agent-table.toml').write_text('''[[agents]]\nrole="manager"\nmanager_id="manager_01"\nmanager_slot="claude-apikey-x"\npool=1\n\n[[agents]]\nrole="reviewer"\nreviewer_id="reviewer_01"\nreviewer_slot="cline-account-x"\npool=9\n''')
    def tearDown(self): self.tmp.cleanup()
    def test_validate_readonly(self):
        before=(self.p/'.freely/agent-table.toml').read_bytes()
        r=self.m.validate(self.p,'reviewer','cline-account-x')
        self.assertTrue(r['ok']); self.assertEqual(before,(self.p/'.freely/agent-table.toml').read_bytes())
        self.assertFalse(self.m.validate(self.p,'nope','x')['ok'])
    def test_apply_only_one_slot(self):
        r=self.m.apply(self.p,'reviewer','cline-account-y')
        self.assertTrue(r['ok']); text=(self.p/'.freely/agent-table.toml').read_text()
        self.assertIn('reviewer_slot="cline-account-y"',text); self.assertIn('manager_slot="claude-apikey-x"',text)
        self.assertTrue(list((self.p/'.freely').glob('agent-table.toml.bak-*')))
    def test_apply_failure_no_write(self):
        before=(self.p/'.freely/agent-table.toml').read_bytes()
        r=self.m.apply(self.p,'reviewer','missing-tool-slot')
        self.assertFalse(r['ok']); self.assertEqual(before,(self.p/'.freely/agent-table.toml').read_bytes())
if __name__=='__main__': unittest.main()
