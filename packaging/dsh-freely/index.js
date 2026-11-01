/** @freely/dsh-freely: DSH harness adapter for a Freely-hosted loop. */
export const name = 'dsh-freely'
export const inject = ['sessionController', 'workspaceRegistry', 'subprocess', 'tools']

const ALLOW = {
  manager: ['read', 'grep', 'glob', 'freely_status', 'freely_worker_start', 'freely_reviewer_start', 'freely_gate'],
  worker: ['read', 'write', 'edit', 'bash', 'grep', 'glob'],
  reviewer: ['read', 'grep', 'glob'],
}

class FreelyBridge {
  constructor(ctx, root) { this.ctx = ctx; this.root = root }
  async run(args, timeoutMs = 30000) {
    const exe = await this.ctx.subprocess.resolveExecutable(`${this.root}/bin/freely`)
    const handle = this.ctx.subprocess.spawn({
      argv: [exe, ...args],
      cwd: this.root,
      stdio: { stdin: 'ignore', stdout: { maxBytes: 65536 }, stderr: { maxBytes: 16384 } },
      graceMs: 5000,
    })
    const { exitCode } = await handle.done
    const stdout = handle.collected.stdout?.readFrom(0)?.text ?? ''
    const stderr = handle.collected.stderr?.readFrom(0)?.text ?? ''
    return { ok: exitCode === 0, exitCode, stdout, stderr }
  }
}

async function createRoleSession(ctx, root, role, preset, allow, task = '') {
  const workspace = await ctx.workspaceRegistry.create(root)
  const sid = `freely-${role}-${Date.now()}-${Math.floor(Math.random() * 1000)}`
  await ctx.sessionController.create({ sessionId: sid, workspaceId: workspace.id, agentPreset: preset })
  const found = await ctx.sessionController.resolveAgent(sid)
  if ('error' in found) throw found.error
  found.agent.ctx.tools.restrict({ allow })
  if (task) found.agent.steer({ id: `msg-${Date.now()}-${Math.floor(Math.random() * 1000)}`, role: 'user', content: [{ type: 'text', text: task }], source: { kind: 'user' } })
  return { sessionId: sid, status: found.agent.status }
}

export async function apply(ctx, config = {}) {
  const root = config.freelyRoot || process.cwd()
  const workspace = await ctx.workspaceRegistry.create(root)
  const sid = config.managerSessionId || `freely-manager-${Date.now()}`
  await ctx.sessionController.create({ sessionId: sid, workspaceId: workspace.id, agentPreset: 'freely-manager' })
  const found = await ctx.sessionController.resolveAgent(sid)
  if ('error' in found) throw found.error
  const agent = found.agent
  const bridge = new FreelyBridge(ctx, root)
  ctx.tools.register({
    name: 'freely_status',
    description: 'Read Freely fleet status for the project.',
    parameters: { type: 'object', properties: {}, additionalProperties: false },
    output: {
      schema: { type: 'object', additionalProperties: true },
      render: (_args, value) => [{ type: 'text', text: JSON.stringify(value) }],
    },
    execute: async () => bridge.run(['fleet-status', '--project', root]),
  })
  ctx.tools.register({
    name: 'freely_worker_start',
    description: 'Create a Freely worker session in the project and optionally send a task.',
    parameters: { type: 'object', properties: { task: { type: 'string' } }, additionalProperties: false },
    output: { schema: { type: 'object', additionalProperties: true }, render: (_a, v) => [{ type: 'text', text: JSON.stringify(v) }] },
    execute: async (args) => createRoleSession(ctx, root, 'worker', 'freely-worker', ALLOW.worker, args?.task || ''),
  })
  ctx.tools.register({
    name: 'freely_reviewer_start',
    description: 'Create a Freely reviewer session in the project and optionally send a task.',
    parameters: { type: 'object', properties: { task: { type: 'string' } }, additionalProperties: false },
    output: { schema: { type: 'object', additionalProperties: true }, render: (_a, v) => [{ type: 'text', text: JSON.stringify(v) }] },
    execute: async (args) => createRoleSession(ctx, root, 'reviewer', 'freely-reviewer', ALLOW.reviewer, args?.task || ''),
  })
  ctx.tools.register({
    name: 'freely_gate',
    description: 'Run pretests-gate for an issue in the project.',
    parameters: { type: 'object', properties: { issue: { type: 'string' } }, required: ['issue'], additionalProperties: false },
    output: { schema: { type: 'object', additionalProperties: true }, render: (_a, v) => [{ type: 'text', text: JSON.stringify(v) }] },
    execute: async (args) => bridge.run(['pretests-gate', '--project', root, '--issue', args.issue]),
  })
  agent.ctx.tools.restrict({ allow: ALLOW.manager })
  ctx.logger?.info?.(`dsh-freely applied root=${root} manager=${sid}`)
  console.log(`[dsh-freely] applied root=${root} manager=${sid}`)
}
