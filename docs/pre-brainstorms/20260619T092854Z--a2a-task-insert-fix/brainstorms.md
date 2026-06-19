# Brainstorm: a2a_task.insert SQL 三重不匹配
## 根因: VALUES 21个? vs 20列名 vs 19个参数, prompt_file缺失
## 影响: 所有A2A task创建失败, Worker委派链路彻底断裂(6月15日起)
## 方案: 补齐prompt_file参数, 修正?数量, 添加测试覆盖
## 决策: promote
