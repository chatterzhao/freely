# IBM Brainstorm

## Why This Issue Exists

旧 contract 只定义了 delegated continuation 何时 generated / consumed / pending after failure，没有定义“本轮已成功产出新 continuity 后，旧 intake 何时结束生命周期”。

## Frozen Boundary

1. 首批只处理 manager-owned local delegated continuation。
2. 只在本轮有新 continuity 文件时 absorbed。
3. continuity judgement 与 intake lifecycle 要分别落真源，但不能长期相互漂移。

## Implementation Direction

1. 在 manager supervisor loop 内比较本轮前后的 latest continuity file。
2. 若本轮 prompt 已吸收 delegated continuation 且 continuity 成功前进，则对匹配 intake 做 `resolve --status absorbed`。
3. 将 resolution artifact 指向本轮 continuity followthrough。
