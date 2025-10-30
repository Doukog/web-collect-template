# 网页数据采集模板

简述：本项目为了减少反复写辣鸡代码而立

## 文件

``` 
web-collect-template/
├── assets/
│   └── config.yaml         运行配置示例
├── config/
│   ├── __init__.py
│   └── config.py           配置封装
├── core/
│   ├── __init__.py
│   └── task.py             采集核心封装，代码在这里编写
├── model/
│   ├── __init__.py
│   └── config.py           配置模型
├── utils/
│   ├── __init__.py
│   └── record.py           记录类
├── .gitignore
├── .python-version
├── main.py                 项目主入口
├── pyproject.toml
├── README.md
└── uv.lock
```

## 功能开发进度

- [x] 数据保存：txt xlsx