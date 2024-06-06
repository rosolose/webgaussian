from django.db import models
from account.models import User

class Ply(models.Model):
    id = models.BigAutoField(primary_key=True) # 主键
    video_path = models.CharField(max_length=255, blank=True, null=True) # 上传存储路径
    flag = models.IntegerField(default=0) # 0视频，1图片文件夹
    ply_path = models.CharField(max_length=255, blank=True, null=True) # 模型存储路径
    upload_time = models.DateTimeField(blank=True, null=True, auto_now_add=True) # 视频上传时间
    ply_time = models.DateTimeField(blank=True, null=True) # 建模完成时间
    is_finished = models.IntegerField(default=0) #  建模状态，0未完成，1已完成

    # 一个用户的多个模型
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plys', blank=True, null=True)

    def __str__(self):
        return str(self.upload_time)

    class Meta:
        db_table = 'ply'
        verbose_name = '模型信息'
        verbose_name_plural = '模型信息'


