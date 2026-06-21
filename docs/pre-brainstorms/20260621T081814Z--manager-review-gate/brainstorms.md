# B1_IBM: Manager review gate + proactive steer

## Discovery
Manager patrol lacks explicit accept/revise judgment for completed workers, and lacks proactive off-track detection for working workers.

## Research
Routa pattern: structured distrust — each lane verifies upstream output. Freely needs accept/revise at Manager level. Dispatch infrastructure (#3208) already provides session/prompt + resume.

## Decision
Add review gate (Step 2) and proactive steer (Step 3) to manager-agent.md prompt. No code changes needed.
