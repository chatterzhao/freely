# Brainstorm: Worker concurrency control
## Problem: unlimited workers, 30 daemons, 200% CPU
## Solution: two-tier cap (7 warn, 10 block) + Manager patrol capacity check
## Decision: promote
