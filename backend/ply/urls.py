from django.urls import path
from .views import upload_videos, upload_images, list_video, list_img
from .views import my_view

urlpatterns = [
    path('upload_videos/', upload_videos),  # 视频上传
    path('upload_images/', upload_images),  # 图片上传
    path('list_video/', list_video),  # 查询模型信息
    path('list_img/', list_img),  # 查询模型信息

    path('my/', my_view), # 个人页面：包含个人信息和个人的模型信息
]