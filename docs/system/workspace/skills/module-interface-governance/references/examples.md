# Examples

## Third-party API version change

- 把第三方 API 视为外部事实源
- 在本地加 adapter，不让上层业务直接依赖提供方细节
- 若 API 升级有破坏性，新增版本化契约并保留回滚路径

## Internal protocol breaking change

- 先定义旧版与新版契约
- 明确迁移窗口和兼容测试
- 在切换完成前，不删除旧版适配层
