/** @freely/dsh-freely: DSH harness adapter for a Freely-hosted loop. */
export const name = 'dsh-freely'
export const inject = ['sessionController', 'workspaceRegistry', 'subprocess', 'tools']

const ALLOW = {
  manager: ['read', 'grep', 'glob'],
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

export async function apply(ctx, config = {}) {
  const root = config.freelyRoot || process.cwd()
  const workspace = await ctx.workspaceRegistry.create(root)
  const sid = config.managerSessionId || `freely-manager-${Date.now()}`
  await ctx.sessionController.create({ sessionId: sid, workspaceId: workspace.id, agentPreset: 'freely-manager' })
  const found = await ctx.sessionController.resolveAgent(sid)
  if ('error' in found) throw found.error
  const agent = found.agent
  agent.ctx.tools.restrict({ allow: ALLOW.manager })
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
  ctx.logger?.info?.(`dsh-freely applied root=${root} manager=${sid}`)
  console.log(`[dsh-freely] applied root=${root} manager=${sid}`)
}
