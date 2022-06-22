### 项目介绍
#### 本系统采用Django+Vue搭建，对于Vue代码部分已经打包，具体可以查看前端代码部分
#### 运行需要配置如下：
1. 安装python3.8版本
2. 安装requests.txt内需要的库
3. 安装mysql和redis，并安装settings.py内修改数据配置、缓冲配置、异步任务配置，
4. 需要在数据库内生成对应的表，具体可以运行school_work.sql文件
5. 数据必须使用已经修改好的数据
#### 运行代码：
 python manage.py runserver
 
 python manage.py qcluster
