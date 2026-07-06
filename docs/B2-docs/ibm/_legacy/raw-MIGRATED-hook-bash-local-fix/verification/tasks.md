# Tasks
1. Remove `local` from `_pid _ppid _cmd _is_wt_close=0` declaration (line 13)
2. Remove `local` from `_full_cmd` declaration (line 19)
3. Add `_is_wt_close=0` as plain assignment outside loop
4. Verify hook works on macOS bash 3.x
