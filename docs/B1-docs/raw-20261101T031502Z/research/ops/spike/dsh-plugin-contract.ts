import type { Context } from '@deepseek-ai/cordis'
import type {} from '@deepseek-ai/dsh-api-session-controller'
import type {} from '@deepseek-ai/dsh-workspace'

export const name = 'freely'
export const inject = ['agents', 'sessionController', 'sessionPersistence', 'workspaceRegistry', 'permissionPresets', 'tools', 'systemPrompt', 'skills', 'llm', 'subprocess']

export function apply(ctx: Context): void {
  // Minimal contract: resolve or create a Freely role session, then prompt it.
  void (async () => {
    const found = await ctx.sessionController.resolveAgent('freely-manager' as never)
    if ('error' in found) {
      const workspace = await ctx.workspaceRegistry.create(process.cwd())
      await ctx.sessionController.create({ sessionId: 'freely-manager' as never, workspaceId: workspace.id, agentPreset: 'freely-manager' })
    }
    ctx.logger.info('freely plugin contract ok')
  })()
}
