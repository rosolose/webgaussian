# WebGaussian
配置Redis    **https://github.com/tporadowski/redis/releases**

```
cd Redis
redis-server.exe  #启动Redis
```

### 启动celery worker和beat

```
celery -A backend worker -l info -P eventlet  #启动celery worker
celery -A backend beat -l info    #启动celery beat
```

celery beat进行任务调度，定时将任务id装载进redis队列中。worker在队列的另一端取出任务id，并匹配当前注册的任务。



### 启动服务器



# 问题&解决

### 1.图片输入过少会创建文件夹，但是有可能无法进行COLMAP，数据库信息存在，导致无法处理。

![image-20240606110249236](assets/image-20240606110249236.png)

​	COLMAP指令报错，将模型的建模状态改为1，完成的状态，先忽略，处理剩余的内容。

​	***Todo：1.在ply类里添加属性。显示模型更多状态。***

### 2.settings.DATA_UPLOAD_MAX_NUMBER_FILES.=100 图片输入过多，上限设置为300。同时会先创建文件夹，但上传数量超出上限，上传不到数据库，会出现空文件夹的情况。

​					![image-20240606110517862](assets/image-20240606110517862.png)

​	先检查文件上传数量再创建文件夹。如果超出上限就报错返回。
