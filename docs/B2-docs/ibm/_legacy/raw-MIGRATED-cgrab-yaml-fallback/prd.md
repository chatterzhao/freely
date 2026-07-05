# PRD: cgrab YAML fallback

## Problem
cgrab() only parsed bullet format. I-* files with YAML frontmatter had all
canonical fields (phase_state, milestone, source_candidate) silently cleared.

## Fix
Add YAML format fallback to cgrab(). Update skill template to bullet format.
