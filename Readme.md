Flask MCV 框架

---

`python` `flask` `MVC`

## 简介

这是关于 Flask 的目录架构模式，采用 WEB 框架中最著名的 MVC
 架构模式，主要采取 Laravel 架构思想，先为最初版本，仅能实现路由与方法相分离，模块与模板相分离。
 
## 目录结构

```
.
├── app  // 框架核心 app 模块
│   ├── Controllers  // 所有控制器文件存放目录，暂不支持多级目录
│       └── IndexController.py  // *控制器文件
│   ├── Models  // *所有模型文件存放目录，暂不支持多级目录
│   ├── __init__.py  // app 模块初始化文件
│   ├── Model.py  // *模型父类文件，公用方法写在这
│   └── Controller.py   // *控制器父类，公用方法可以写在这
├── configs  // 配置文件夹，功能暂未实现
├── library  // 第三方包和自定义包，文件夹，功能暂未实现
├── public  // 静态文件夹
│   ├── css
│   └── js
├── routes  // 路由模块
│   ├── __init__.py  // 路由初始化
│   └── web.js  // *路由书写位置
├── templates  // 模板文件夹
│   ├── index // 根据控制器分类模板
│       └── index.html  // 模板具体文件
├── tests  // 测试文件夹
├── venv  // python 第三方包，此文件夹，下载后，自行生成
├── index.py  // 入口文件
├── setup.py  // 包依赖管理文件
├── uwsgi.ini  // uwsgi web 服务配置文件
└── Readme.md
```

> 目录结构中标星的是要创建和编辑的文件

## 控制器示例

> ./app/Controllers/IndexController.py

```python
from app import Application

@Application.embellish
def index(app):
    return app.view('index/index')
```

## 路由示例

> ./routes/web.py

```python
from routes import Route

Route.get('/', 'IndexController@index')
```

## 模板示例

> ./templates/index/index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    Hello World !!!
</body>
</html>
```

## 最后

装好 flask 虚拟运行环境，装好 flask，命令行运行

```shell
flask run
```

> 这时候访问 `http://127.0.0.1:5000`
> 
> 你应该会看到浏览器输出 `Hello World!!!` 字样
