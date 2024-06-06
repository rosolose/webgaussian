import os
import shutil
import time
from datetime import datetime

from django.db import transaction
import pymysql  # 连接数据库
import django
import uuid  # 生成随机数，用于设置唯一标志
# import gaussian_splatting.train # 需要把3dgs作为一个包调用，需要自己定义接口函数，在这个文件里实现对3dgs建模的调用与建模
import subprocess
from django.http import HttpResponse
from django.db import models


"""gaussian这块需要自己去建立数据库连接，使用pymysql"""
host = 'localhost'
port = 3306
db = 'webgs'
user = 'root'
password = '123456'


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# django.setup()

def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn


# 复制文件函数：将storage中的内容复制到gaussian_splatting下去执行
def copyfile(srcfile, dstpath):       #srcfile=
    if not os.path.exists(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fname = srcfile.split('/')[-1]  # 分离文件名和路径
        dstpath = os.path.join(dstpath, fname, 'input')
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        file_list = os.listdir(srcfile)
        for image in file_list:
            source_path = os.path.join(srcfile, image)
            target_path = os.path.join(dstpath, image)
            shutil.copy(source_path,target_path)  # 复制文件
            print("copy %s -> %s" % (source_path, target_path))


def train_view(source_path, mode_path):
    if source_path and mode_path:
        try:
            # 构建命令行命令
            command1 = ['python', 'gaussian_splatting/convert.py', '-s', source_path]
            # 运行脚本
            process1 = subprocess.run(command1, stdout=subprocess.PIPE, text=True)
        except Exception as e:
            print(e)
            from ply.models import Ply
            img_ply = Ply(is_finished = 1)
            img_ply.save()
            return HttpResponse("图片过少，无法进行colmap")
        try:
            command2 = ['python', 'gaussian_splatting/train.py', '-s', source_path, '-m', mode_path]
            process2 = subprocess.run(command2, stdout=subprocess.PIPE, text=True)
        except Exception as e:
            print(e)
            return HttpResponse(f"Training started with source {source_path} and mode {mode_path}. Output:\n{process2.stdout}")
    else:
        return HttpResponse("Missing 'source' or 'mode' parameter")


def gaussian_train():
    """1、建立数据库连接"""
    conn = get_connection()

    """2、进行数据库查询，获取所有数据项"""
    cursor = get_connection().cursor()
    query = ('select * from ply')
    cursor.execute(query)
    results = cursor.fetchall()

    """3、判断每一项是否建模，进行建模"""

    for result in results:
        video_path = result[1]

        if result[-1] == 1:
            continue
        if result[2] == 0:
            command = ['ffmpeg', '-i', 'source_path', '-vf', '"setpts=0.2*PTS"', "source_path+'input_%4d.jpg'"]
            process = subprocess.run(command, stdout=subprocess.PIPE, text=True)
        srcfile = '/'.join(video_path.split('/')[:-1])
        copyfile(srcfile, 'gaussian_splatting/data/')
        #取input作为输入
        fname = video_path.split('/')[-2]
        source_path = os.path.join('gaussian_splatting/data',fname)
        origin_output_path = os.path.join('storage/output/', fname)
        try:
            # 尝试运行 train_view 函数
            train_view(source_path, origin_output_path)
            from ply.models import Ply
            img_ply = Ply(ply_path = os.path.join(origin_output_path,'output'),
                          ply_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          is_finished = 1)
            img_ply.save()
            print("train_view 函数执行成功！")
            # 这里可以放置更多函数成功运行时需要执行的代码
        except Exception as e:
            # 如果函数抛出了异常，执行这段代码
            print("train_view 函数执行失败！")
            print(f"错误信息：{e}")
            from ply.models import Ply
            img_ply = Ply(is_finished=1)
            img_ply.save()


if __name__ == "__main__":
    gaussian_train()

    # todo:单线程运行检测，定时检测服务，返回数据库

    # todo:自动检测运行，上传完数据发送请求，检查当前是否在运行（线程检测）

    # 使用目录复制/文件复制，把storage目录下的文件复制到gaussian_splatting 的输入目录下
    # （比如从stotage/upload_images/...到gaussian_splatting/.../0/这个目录下，记不清了好像是这样的。图片的是这种)

    # 然后控制台输出“开始对...建模”的消息，调用原来gaussian_splatting里面的train.py函数，它就会自己去找到并建模
    # 因为这个过程是阻塞的，所以一直在运行，最后输出到它自己的output文件夹里面

    # gaussian_splatting.train.strat()

    # 然后我们读取生成好的文件，把它复制到storage/output里面

    """4、数据库操作"""


