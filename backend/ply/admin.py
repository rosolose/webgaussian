from django.contrib import admin
from .models import Ply
# Register your models here.

class PlyAdmin(admin.ModelAdmin):
    list_display = ('video_path', 'upload_time','is_finished','owner')
    
admin.site.register(Ply, PlyAdmin)