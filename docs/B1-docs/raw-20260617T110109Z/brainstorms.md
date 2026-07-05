# Brainstorm: Remove prompt_file from A2A Layer
## Discovery
A2A protocol standard uses Message.parts[{text}] for content, never files.
prompt_file in A2A Task is ACP implementation detail leaking into wrong layer.
Subagent review confirmed APPROVE WITH CHANGES.
## Decision
Promote. Remove from 6 files. prompt_file path derived from task_id at Runtime.
