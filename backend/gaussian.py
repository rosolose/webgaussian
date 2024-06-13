import shutil
import datetime
import pymysql  # 连接数据库
import subprocess
from django.http import HttpResponse
from django.db import models
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from ply.models import Ply

#
# """gaussian这块需要自己去建立数据库连接，使用pymysql"""
# host = 'localhost'
# port = 3306
# db = 'webgs'
# user = 'root'
# password = '123456'
# def get_connection():
#     conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
#     return conn


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

    plys = Ply.objects.filter(is_finished=0)
    for ply in plys:
        video_path = ply.video_path

        if ply.flag == 0:
            command = ['ffmpeg', '-i', 'video_path', '-vf', '"setpts=0.2*PTS"', "video_path+'input_%4d.jpg'"]
            process = subprocess.run(command, stdout=subprocess.PIPE, text=True)

        #在gaussian_splatting/data下中创建同名文件夹作为输入input
        srcfile = '/'.join(video_path.split('/')[:-1])
        copyfile(srcfile, 'gaussian_splatting/data/')
        fname = video_path.split('/')[-2]
        source_path = os.path.join('gaussian_splatting/data',fname)
        origin_output_path = os.path.join('storage/output/', fname)
        try:
            # 尝试运行 train_view 函数
            train_view(source_path, origin_output_path)
            ply.ply_path = os.path.join(origin_output_path,'output',fname,'point_cloud','iteration_30000','point_cloud.ply')
            ply.ply_time = datetime.datetime.now()
            ply.is_finished = 1
            ply.save()
            print("train_view 函数执行成功！")
            # 这里可以放置更多函数成功运行时需要执行的代码
        except Exception as e:
            # 如果函数抛出了异常，执行这段代码
            print("train_view 函数执行失败！")
            ply.is_finished = 1
            ply.save()
            print(f"错误信息：{e}")


if __name__ == "__main__":
    gaussian_train()




