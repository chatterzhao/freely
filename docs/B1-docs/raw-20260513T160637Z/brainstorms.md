# Brainstorm: backtick command substitution in start-lead-agent.sh

<<EOF without quotes causes backticks to be interpreted as command substitution.
Fix: use plain string with proper backslash escaping.
