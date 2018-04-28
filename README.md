# zlbbs
### 第一步:搭建目录结构
+  cms、front、common三个分别存放对应的models、views、forms
+  ueditor 引入编辑器
+  migrations 数据库迁移文件
+  static 存放cms、front、common静态资源
+  templates 存放cms、front、common模板文件
+  utils 存放工具类
+  config 配置文件
+  exts 引入的第三方库
+  manage.py 数据库操作相关
+  zlbbs.py 主运行文件

### 第二步:创建蓝图并在主文件中注册


### 第三步:配置数据库相关信息
+  配置信息
```python
USERNAME='root'
PASSWORD=''
HOST='127.0.0.1'
PORT='3306'
DATABASE='zlbbs' //先在数据库创建好
DB_URI='mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8'.format(username=USERNAME,password=PASSWORD,host=HOST,port=PORT,db=DATABASE)

SQLALCHEMY_DATABASE_URI=DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS=False //不跟踪sqlAlchemy中的模型
```

+  创建用户模型
+  在manage.py中创建管理数据库的相关函数

(未完待续...)
