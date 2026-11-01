import test from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, readFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { apply } from '../driver.js'

test('driver creates worker/reviewer, commits, writes result', async () => {
  const repo = await mkdtemp(join(tmpdir(), 'dsh-e2e-'))
  const calls = { create: [], steer: [], spawn: [] }
  const agent = (sid) => ({ id: sid, status: 'idle', ctx: { tools: { restrict: () => {} } }, steer: (x) => calls.steer.push(x) })
  const ctx = {
    sessionController: {
      create: async (x) => { calls.create.push(x); return x },
      resolveAgent: async (sid) => ({ agent: agent(sid) }),
    },
    workspaceRegistry: { create: async (root) => ({ id: 'ws-' + root }) },
    subprocess: {
      resolveExecutable: async () => '/bin/bash',
      spawn: (x) => { calls.spawn.push(x); return { done: Promise.resolve({ exitCode: 0 }), collected: { stdout: { readFrom: () => ({ text: 'abc e2e\n' }) }, stderr: { readFrom: () => ({ text: '' }) } } } },
    },
  }
  await apply(ctx, { repo, timeoutMs: 2000 })
  assert.equal(calls.create.length, 2)
  assert.equal(calls.create[0].agentPreset, 'freely-e2e-worker')
  assert.equal(calls.create[1].agentPreset, 'freely-e2e-reviewer')
  assert.ok(calls.steer[0].content[0].text.includes('git commit'))
  const result = JSON.parse(await readFile(join(repo, 'result.json'), 'utf8'))
  assert.equal(result.committed, true)
  assert.match(result.commit, /e2e/)
})
