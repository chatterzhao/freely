import test from 'node:test'
import assert from 'node:assert/strict'
import { apply } from '../index.js'

function fakeCtx() {
  const calls = { create: [], restrict: [], tools: [], spawn: [] }
  const agent = { id: 's1', ctx: { tools: { restrict: (x) => calls.restrict.push(x) } } }
  return {
    calls,
    ctx: {
      workspaceRegistry: { create: async (root) => ({ id: 'ws-' + root }) },
      sessionController: {
        create: async (x) => { calls.create.push(x) },
        resolveAgent: async () => ({ agent }),
      },
      subprocess: {
        resolveExecutable: async () => '/bin/bash',
        spawn: (x) => { calls.spawn.push(x); return { done: Promise.resolve({ exitCode: 0 }), collected: { stdout: { readFrom: () => ({ text: 'fleet-ok' }) } } } },
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
  assert.deepEqual(calls.restrict[0].allow, ['read', 'grep', 'glob'])
  assert.equal(calls.tools[0].name, 'freely_status')
})

test('freely_status executes bridge', async () => {
  const { ctx, calls } = fakeCtx()
  await apply(ctx, { freelyRoot: '/tmp/freely' })
  const result = await calls.tools[0].execute({}, { signal: new AbortController().signal })
  assert.match(JSON.stringify(result), /fleet-ok/)
  assert.ok(calls.spawn[0].argv.join(' ').includes('fleet-status'))
})
