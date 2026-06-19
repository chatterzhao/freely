# Brainstorm: worker task message newlines break consume_delegate_workers
## Root cause: message field has 11+ \\n chars, breaks tab-separated line format
## Fix: squash newlines to spaces before printing
## Decision: promote
