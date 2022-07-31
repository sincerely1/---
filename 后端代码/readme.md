### 项目介绍
#### 本系统采用Django+Vue搭建，对于Vue代码部分已经打包，具体可以查看前端代码部分
#### 运行需要配置如下：
1. 安装python3.8版本
2. 安装requests.txt内需要的库
3. 安装mysql5.7和redis
4. 依据配置的数据库接口修改settings.py内修改数据配置（DATABASES）、缓冲配置（CACHES）、异步任务配置（Q_CLUSTER），
5. 需要在数据库内生成对应的表，具体可以运行school_work.sql文件
#### 运行代码：
 python manage.py runserver
 
 python manage.py qcluster

 #### 具体使用
 1. 登陆Django自带的后端系统创建管理员，或者通过数据库创建管理员，也可以创建和修改学生、教师等用户
 2. 通过管理员可以使用管理员页面修改和创建学生、教师
 3. 教师创建课程后，可以上传材料，提交学生的答题信息，具体提交格式可以参考zip
 4. _data/demo/demo.zip，由于系统存在不足，没有办法通过教学系统直接获取对应的题目知识点和难度信息，需要补全所以需要创建<class_name>题目知识点和难度重设.xlsx文件，具体填写参考下表
   ![难度等级分析.PNG](https://s2.loli.net/2022/07/31/DB1gl7yJfmAVczS.png)