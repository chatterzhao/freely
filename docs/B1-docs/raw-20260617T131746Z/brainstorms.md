# Brainstorm: Fix pull || true
## Discovery
gh pr merge creates merge commit on GitHub. Local pull --ff-only with || true silently fails. Next push no-ops or non-fast-forward. Root cause of manual git push after pr-merge-guarded.
## Decision
Promote. Replace || true with fetch+reset fallback.
