# your_project/your_project/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 为celery程序设置Django的settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend',backend='redis://127.0.0.1:6379/1', broker='redis://127.0.0.1:6379/0')

# 使用Django的settings文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现各个app下的任务 (tasks.py)
app.autodiscover_tasks()