# Tasks — raw-20261114T101138Z

- [x] T1: `platform-adapter.py` 新增 `close_dropped`（先写关闭评论再 not-planned 关单，评论失败不关任何平台）；`close_issue` 及两 handler 扩展默认参数（既有调用零改动）；CLI 新增 `close-dropped` 分派
- [x] T2: `wt-close` `--force` 分支编排 `transition("dropped")` 瞬时本地态 → 组装关闭评论（理由 + B1 研究）→ `close-dropped`，加 `--dry-run` 守卫
- [x] T3: `pull_raw_issue` 全 CLOSED 副本 fail-closed 防重新物化
- [x] T4: 新增 AT `test-wt-close-dropped-closeout.py`（7/7 OK），CORE/CI_CORE 各 +1；回归既有测试全绿
- [x] T5: promote → absorb → governance gate → pr-create → review → merge → wt-close
