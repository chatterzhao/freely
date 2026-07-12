# B1: config.toml.example allowed_paths TOML format
## Problem
多行注释在 TOML 数组内导致 freely init 解析后写成字符串 "[]"
## Decision
改为单行空数组，注释移到上方
