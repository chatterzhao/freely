# PRD: 打包 parity 回归收口
## Goal
恢复 install-state 打包能力，且不推翻 commands.md 不随包发布的既有判决。
## 实现方案
- bin/freely 注释去掉字面文档路径，只写真实命令。
- command_name_contract.py 移到 scripts/tests/；AT 与函数级单测改引用路径。
## Dev-Loop Handoff
先 RED 复现 parity rc=1，再改，最后 GREEN + 打包实测。
