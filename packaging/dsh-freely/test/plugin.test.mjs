import test from 'node:test'
import assert from 'node:assert/strict'
import { apply } from '../index.js'

function fakeCtx({ failExecutable = false } = {}) {
  const calls = { create: [], restrict: [], tools: [], spawn: [], steer: [] }
  const agent = { id: 's1', status: 'idle', ctx: { tools: { restrict: (x) => calls.restrict.push(x) } }, steer: (x) => calls.steer = x }
  return {
    calls,
    ctx: {
      workspaceRegistry: { create: async (root) => ({ id: 'ws-' + root }) },
      sessionController: {
        create: async (x) => { calls.create.push(x) },
        resolveAgent: async () => ({ agent }),
      },
      subprocess: {
        resolveExecutable: async () => { if (failExecutable) throw new Error('missing bin/freely'); return '/bin/bash' },
        spawn: (x) => {
          calls.spawn.push(x)
          return { done: Promise.resolve({ exitCode: 0 }), collected: { stdout: { readFrom: () => ({ text: 'fleet-ok' }) }, stderr: { readFrom: () => ({ text: '' }) } } }
        },
      },
      tools: { register: (x) => calls.tools.push(x) },
      effect: () => () => {},
      logger: { info: () => {} },
    },
  }
}

test('apply creates manager session and restricts tools', async () => {
  const { ctx, calls } = fakeCtx()
  await apply(ctx, { freelyRoot: '/tmp/freely' })
  assert.equal(calls.create[0].agentPreset, 'freely-manager')
  assert.deepEqual(calls.restrict[0].allow, ['read', 'grep', 'glob', 'freely_status', 'freely_worker_start', 'freely_reviewer_start', 'freely_gate'])
  assert.deepEqual(calls.tools.map((t) => t.name), ['freely_status', 'freely_worker_start', 'freely_reviewer_start', 'freely_gate'])
})

test('freely_status executes bridge', async () => {
  const { ctx, calls } = fakeCtx()
  await apply(ctx, { freelyRoot: '/tmp/freely' })
  const result = await calls.tools.find((t) => t.name === 'freely_status').execute({}, { signal: new AbortController().signal })
  assert.match(JSON.stringify(result), /fleet-ok/)
  assert.ok(calls.spawn[0].argv.join(' ').includes('fleet-status'))
})

test('worker/reviewer sessions restrict role tools', async () => {
  const { ctx, calls } = fakeCtx()
  await apply(ctx, { freelyRoot: '/tmp/freely' })
  const worker = await calls.tools.find((t) => t.name === 'freely_worker_start').execute({ task: 'do work' })
  const reviewer = await calls.tools.find((t) => t.name === 'freely_reviewer_start').execute({ task: 'review' })
  assert.match(worker.sessionId, /^freely-worker-/)
  assert.match(reviewer.sessionId, /^freely-reviewer-/)
  assert.deepEqual(calls.restrict[1].allow, ['read', 'write', 'edit', 'grep', 'glob'])
  assert.deepEqual(calls.restrict[2].allow, ['read', 'grep', 'glob'])
  assert.equal(calls.create[1].agentPreset, 'freely-worker')
  assert.equal(calls.create[2].agentPreset, 'freely-reviewer')
})

test('freely_gate returns exit code and fail-closed on missing executable', async () => {
  const { ctx, calls } = fakeCtx()
  await apply(ctx, { freelyRoot: '/tmp/freely' })
  const gate = await calls.tools.find((t) => t.name === 'freely_gate').execute({ issue: 'x.md' })
  assert.equal(gate.ok, true)
  assert.equal(gate.exitCode, 0)

  const broken = fakeCtx({ failExecutable: true })
  await assert.rejects(() => apply(broken.ctx, { freelyRoot: '/tmp/freely' }), /missing bin\/freely/)
})
