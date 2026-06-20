# Brainstorm: PR #3147 regression — silent daemon crash
## Root cause: 2 callers unchecked for old 'unbounded' format
## Fix: parse max:warn in all callers
## Decision: promote
