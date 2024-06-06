import pymysql

pymysql.install_as_MySQLdb()

# 这将确保app在Django启动时启动
from .celery import app as celery_app

__all__ = ('celery_app',)