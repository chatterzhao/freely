# Brainstorm: sup_pid_file unbound variable

start_project_runtime uses sup_pid_file at cleanup but never defines it.
