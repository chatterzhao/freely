# Brainstorms - 20260426-0002--break-glass-agents-guidance

## Problem
AGENTS.md line 114 used soft language ("若确实命中 break-glass") that allowed AI to rationalize false bypass justifications. During real dogfooding, two develop merges used break-glass to bypass documentation gaps that should have been fixed.

## Decision
Harden the guidance: explicitly list common false justifications, narrow verified_false_negative to factual errors only, and make the default stance clearer.
