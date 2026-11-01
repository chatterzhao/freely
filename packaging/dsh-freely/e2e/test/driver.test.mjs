import test from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, readFile, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { apply } from '../driver.js'

test('driver creates worker/reviewer, commits, writes result', async () => {
  const repo = await mkdtemp(join(tmpdir(), 'dsh-e2e-'))
  const calls = { create: [], steer: [], spawn: 0 }
  const agent = (sid) => ({
    id: sid, status: 'idle', ctx: { tools: { restrict: () => {} } },
    steer: async (x) => {
      calls.steer.push(x)
      if (String(x.content?.[0]?.text || '').includes('VERDICT.txt')) await writeFile(join(repo, 'VERDICT.txt'), 'pass')
    },
  })
  const ctx = {
    sessionController: {
      create: async (x) => { calls.create.push(x); return x },
      resolveAgent: async (sid) => ({ agent: agent(sid) }),
    },
    workspaceRegistry: { create: async (root) => ({ id: 'ws-' + root }) },
    subprocess: {
      resolveExecutable: async () => '/bin/bash',
      spawn: (x) => {
        calls.spawn++
        let out = 'abc e2e\n'
        if (x.argv.includes('rev-parse')) out = calls.spawn === 1 ? 'base\n' : 'e2e-commit\n'
        return { done: Promise.resolve({ exitCode: 0 }), collected: { stdout: { readFrom: () => ({ text: out }) }, stderr: { readFrom: () => ({ text: '' }) } } }
      },
    },
  }
  await apply(ctx, { repo, timeoutMs: 2000, project: '/tmp', issue: 'x.md' })
  assert.equal(calls.create.length, 2)
  assert.equal(calls.create[0].agentPreset, 'freely-e2e-worker')
  assert.equal(calls.create[1].agentPreset, 'freely-e2e-reviewer')
  assert.ok(calls.steer[0].content[0].text.includes('git commit'))
  const result = JSON.parse(await readFile(join(repo, 'result.json'), 'utf8'))
  assert.equal(result.committed, true)
  assert.equal(result.reviewerVerdict, 'pass')
})
