from django.contrib import admin
from django.urls import path,re_path, include
from django.views.static import serve
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('ply/', include('ply.urls')),
    re_path('storage/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}) # 前端访问后端资源文件
]
