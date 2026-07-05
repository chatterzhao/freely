# Brainstorm: bridge disconnect fix (GitHub #187)

run-acp-prompt.py disconnects before bridge finishes sending session/update
notifications, causing [Errno 32] Broken pipe → false rc=1 → restart storm.

Fix: end_turn grace period + broken pipe tolerance.
