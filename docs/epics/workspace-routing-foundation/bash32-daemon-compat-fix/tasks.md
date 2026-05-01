# Tasks: bash32-daemon-compat-fix

1. Fix daemon self-detection suicide by excluding $$ from supervisor pid discovery.
2. Fix bash 3.2 pipefail crash in select_launch_kind by replacing bare ls glob with nullglob-guarded array.
