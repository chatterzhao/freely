# PRD: A2A server h11 noise suppression

## Problem
h11 emits WARNING for every non-HTTP byte. Content-Length bug fixed, remaining noise from external probes.

## Fix
Custom uvicorn log_config: h11 logger at ERROR level. Keeps uvicorn at INFO.
