# Brainstorm: launch function produces no output
## set -euo pipefail may cause silent exits before any log call
## Fix: add log_info at each return point
## Decision: promote
