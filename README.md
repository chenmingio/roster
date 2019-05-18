## 目的

用于记录部门员工某一周的值勤情况

## 后端

### Data Definition

table records

time name location

### 工具链

sqlite + bottle


## 前端

### React


## 经验总结

需要尽快学会单元测试.测试的输入的内容需要考虑的实际过程中可能产生的格式.同时使用logging模块,不然服务器莫名其妙坏了,都不知道原因.

在数据库/基本数据结构上走了点弯路.以后设计要现在纸上多花时间,思考不同方案之间的pros n cons.

nginx基本的static文件设置还需要实验下.

## Timelog

### 20190510 

* 在大脑中完成数据设计和restful设计 1h
+ 后端50% 2h
* 试图使用heroku 0.5h

### 20190511

* 研究heroku,发现不支持sqlite3(每天会清空) 1h
* 再次阅读full stack deployment 并部署 3h
* 完成剩下的50%后端工作

### 20190611

* 把api的输出format优化为json格式.参考文档 [Python: SQL to JSON and beyond! – Charles Stauffer – Medium](https://medium.com/@PyGuyCharles/python-sql-to-json-and-beyond-3e3a36d32853)


