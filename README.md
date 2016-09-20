# Bubblegum

Bubblegum 是一个大二时写的基于flask实现的论坛, 前端界面写的挺丑的, 现在有重构的计划, 请戳[这里](https://github.com/getquillapp/quill)

## 截图

![screenshot](/screenshots/screenshot.png)


## 使用

```
$ sudo pip install virtualenv
$ git clone git@github.com:gaotongfei/bubblegum.git && cd bubblegum
$ virtualenv venv && source venv/bin/activate
$ pip install -r requirements.txt
```

```
$ python manager.py createdb      # 在本地创建sqlite3数据库
$ python manager.py runserver     # 运行程序
```


访问[http://127.0.0.1:5000/](http://127.0.0.1:5000/)