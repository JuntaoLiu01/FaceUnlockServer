服务端设计
========
the  server of [FaceUnlock](https://github.com/hzshang/FaceUnlock)
## 用户管理  
服务端为每一部手机生成一个 token 标识，并创建文件夹用来存储该手机用户的人脸图像编码。这里并没有选择直接存储图像，一是考虑到图像文件过大，存储空间要求较高；二是在验证时需要重新读取图像，计算编码，效率较低。数据库中存储文件路径，用于查找、增加、删除用户。
## 接口实现  
服务端和客户端进行5种类型的交互，POST 参数格式如下:
  
|－|DETECT|CREATE_SET|ADD_FACE|SEARCH_FACE|DELETE_FACE
|---|:-----:|:---------:|:----:|:----:|:----:|
|URL|~/detect|~/create|~/addface|~/search|~/removeface
|PARM_1|api_key|api_key|api_key|api_key|api_key
|PARM_2|image_file|-|face_token|faceset_token|face_token
|PARM_3|-|-|faceset_token|image_file|-| 
### 人脸检测  
用户上传人脸图像，服务端进行人脸检测，如果图像符合要求，则为该人脸创建 token 标识，存储编码文件，并在数据库中加入一条记录。返回数据格式如下：  
  
```  
 {
        "faces":[
            {
                "face_rectangle": {
                    "width": 140,
                    "top": 89,
                    "left": 104,
                    "height": 141
                    },
                "face_token": "ed319e807e039ae669a4d1af0922a0c8"
            }
 }  
```     
### 创建人脸集  
用户向服务端发起请求，服务端为客户端手机生成 token 标识并创建人脸集。返回数据格式：  

```
{
    "faceset_token": "ed319e807e039ae669a4d1af0922a0c8"
}
```
### 添加人脸
用户上传人脸标识 `face_token` 以及人脸集标识 `faceset_token`，如果token存在，那么将人脸图像编码加入人脸集中，并在数据库中更改相应记录。  
### 人脸比对  
用户解锁手机时，服务端会将拍摄的照片上传，服务端在将验证图像编码和人脸集中的图像编码进行比对，计算得到响应的置信度。返回数据格式:  

```
{
	"results":[{
   		"confidence":85.9,
   		"face_token":"ed319e807e039ae669a4d1af0922a0c8"
	},{
   		"confidence":35.9,
    	"face_token":"ed319e807e039ae669a4d1a98gc2nmkv"
	}]
}
``` 
### 删除人脸  
根据用户上传的 `face_token` ，服务端删除相应的人脸图像编码文件，并在数据库中去除一条记录。
=======
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

