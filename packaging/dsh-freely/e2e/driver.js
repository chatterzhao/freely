/** Deterministic DSH E2E driver for @freely/dsh-freely. Test-only. */
import { readFile, rm, writeFile } from 'node:fs/promises'
import { join } from 'node:path'

export const name = 'dsh-freely-e2e'
export const inject = ['sessionController', 'workspaceRegistry', 'subprocess', 'tools']

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function waitIdle(ctx, sid, timeoutMs = 60000) {
  const deadline = Date.now() + timeoutMs
  let last = 'unknown'
  while (Date.now() < deadline) {
    const found = await ctx.sessionController.resolveAgent(sid)
    if (!('error' in found)) {
      last = found.agent.status || 'unknown'
      if (last === 'idle') return last
    }
    await sleep(1000)
  }
  throw new Error(`session ${sid} not idle (last=${last})`)
}

async function git(ctx, repo, args) {
  const exe = await ctx.subprocess.resolveExecutable('git')
  const handle = ctx.subprocess.spawn({
    argv: [exe, '-C', repo, ...args],
    cwd: repo,
    timeoutMs: 15000,
    stdio: { stdin: 'ignore', stdout: { maxBytes: 8192 }, stderr: { maxBytes: 8192 } },
    graceMs: 3000,
  })
  const { exitCode } = await handle.done
  return {
    ok: exitCode === 0,
    exitCode,
    stdout: handle.collected.stdout?.readFrom(0)?.text ?? '',
    stderr: handle.collected.stderr?.readFrom(0)?.text ?? '',
  }
}

export async function apply(ctx, config = {}) {
  const repo = config.repo
  if (!repo) throw new Error('e2e config.repo required')
  await rm(join(repo, 'DONE.txt'), { force: true })
  await rm(join(repo, 'VERDICT.txt'), { force: true })
  await rm(join(repo, 'result.json'), { force: true })
  const workspace = await ctx.workspaceRegistry.create(repo)
  const before = await git(ctx, repo, ['rev-parse', 'HEAD'])

  const workerTask = config.workerTask || `In ${repo}, create DONE.txt containing ok, then run git add DONE.txt and git commit -m e2e in that directory. Do not ask.`
  const workerSid = `e2e-worker-${Date.now()}`
  await ctx.sessionController.create({ sessionId: workerSid, workspaceId: workspace.id, agentPreset: 'freely-e2e-worker' })
  const wf = await ctx.sessionController.resolveAgent(workerSid)
  if ('error' in wf) throw wf.error
  wf.agent.ctx.tools.restrict({ allow: ['read', 'write', 'edit', 'bash', 'grep', 'glob'] })
  wf.agent.steer({ id: `msg-w-${Date.now()}`, role: 'user', content: [{ type: 'text', text: workerTask }], source: { kind: 'user' } })
  await waitIdle(ctx, workerSid, config.timeoutMs || 60000)

  const log = await git(ctx, repo, ['log', '-1', '--oneline'])
  const after = await git(ctx, repo, ['rev-parse', 'HEAD'])
  const committed = before.ok && after.ok && before.stdout.trim() !== after.stdout.trim() && /e2e/.test(log.stdout)

  const reviewerSid = `e2e-reviewer-${Date.now()}`
  await ctx.sessionController.create({ sessionId: reviewerSid, workspaceId: workspace.id, agentPreset: 'freely-e2e-reviewer' })
  const rf = await ctx.sessionController.resolveAgent(reviewerSid)
  if ('error' in rf) throw rf.error
  rf.agent.ctx.tools.restrict({ allow: ['read', 'write', 'bash', 'grep', 'glob'] })
  rf.agent.steer({ id: `msg-r-${Date.now()}`, role: 'user', content: [{ type: 'text', text: `Review ${repo}: run git log -1 --oneline and git show --stat HEAD; if DONE.txt exists and the diff is only DONE.txt, write VERDICT.txt containing pass and reply exactly VERDICT: pass.` }], source: { kind: 'user' } })
  await waitIdle(ctx, reviewerSid, config.timeoutMs || 60000)

  let reviewerVerdict = null
  try { reviewerVerdict = (await readFile(join(repo, 'VERDICT.txt'), 'utf8')).trim() } catch {}

  let gate = { ok: false, exitCode: null, stdout: '', stderr: 'not configured' }
  if (config.project && config.issue) {
    const exe = await ctx.subprocess.resolveExecutable(`${config.project}/bin/freely`)
    const h = ctx.subprocess.spawn({ argv: [exe, 'pretests-gate', '--project', config.project, '--issue', config.issue], cwd: config.project, timeoutMs: 30000, stdio: { stdin: 'ignore', stdout: { maxBytes: 8192 }, stderr: { maxBytes: 8192 } }, graceMs: 3000 })
    const { exitCode } = await h.done
    gate = { ok: exitCode === 0, exitCode, stdout: h.collected.stdout?.readFrom(0)?.text ?? '', stderr: h.collected.stderr?.readFrom(0)?.text ?? '' }
  }

  const result = { repo, workerSessionId: workerSid, reviewerSessionId: reviewerSid, committed, commit: log.stdout.trim(), reviewerVerdict, gateExitCode: gate.exitCode, gateOk: gate.ok }
  await writeFile(join(repo, 'result.json'), JSON.stringify(result, null, 2))
  console.log(`[dsh-freely-e2e] ${JSON.stringify(result)}`)
  if (!committed || reviewerVerdict !== 'pass' || !gate.ok) throw new Error(`e2e failed: ${JSON.stringify(result)}`)
}
