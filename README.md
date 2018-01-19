## FaceUnlockServer

[FaceUnlock](https://github.com/hzshang/FaceUnlock)的服务端

## 配置

- 将config文件夹中的db.sql导入数据库
- 将config文件夹中的config-sample.json 更名为config.json 并进行配置


## 运行

使用到的python库  

- face_recongition
- pymysql
- Flask

安装完成后运行 python app.py

或者
### 使用Docker安装(安装依赖库时间较长)

	cd ./
	docker build -t app:latest .

运行示例

	docker run -d -p 5002:5002 --name faceunlock app:latest

## 设计文档
[服务端设计](doc/服务端设计.md)


