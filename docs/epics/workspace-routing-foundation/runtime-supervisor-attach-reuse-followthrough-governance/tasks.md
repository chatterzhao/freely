# Tasks - runtime-supervisor-attach-reuse-followthrough-governance

1. Reuse a healthy same-project supervisor from repeated `freely daemon start` instead of relaunching another detached daemon-run process.
2. Attach foreground `freely start` to a live supervisor between AI cycles when runtime truth still says the project should remain running.
3. Preserve that attach path when `ps` is unavailable but cwd ownership still proves the runtime belongs to the same project.
4. Isolate Claude launcher `HOME` under the project runtime directory.
5. Write focused verification and keep the owner bound to this checkpoint worktree.
