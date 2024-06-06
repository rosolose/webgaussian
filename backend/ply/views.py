import os
import uuid
import datetime
from django.core.files.storage import FileSystemStorage

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import jwt_required

from utils.const import StorageConst
from .models import Ply
from account.models import User

# 上传视频
@csrf_exempt  # 不使用CSRF保护
def upload_videos(request):
    if request.method == 'POST' and request.FILES['video']:
        video = request.FILES['video']
        # 视频保存，如果文件名已经存在，Django 会自动添加随机字符串
        fs = FileSystemStorage(location=StorageConst.UploadVideo)
        filename = fs.save(video.name, video)
        # 文件存储路径+视频名称
        # uploaded_file_path = StorageConst.UploadVideo + fs.url(filename)
        uploaded_file_path = StorageConst.UploadVideo + '/' + filename

        # todo：插入数据库信息：（id），视频保存路径，用户id，处理状态为0
        video_ply = Ply(video_path=uploaded_file_path,
                        )
        video_ply.save()

        return JsonResponse({'code': 200,
                             'msg': 'success upload video',
                             'data': uploaded_file_path})  # 返回视频存储路径
    return JsonResponse({'code': 404, 'msg': 'failed to upload images', 'data': None})


# 上传图片
@csrf_exempt
def upload_images(request):
    if request.method == 'POST':

        max_files = 300
        # 检查上传的文件数量
        files = request.FILES.getlist('images')  #对应ImageUploader中formData.append中的key值
        if len(files) > max_files:
            return HttpResponse("错误：上传的文件数量超过了限制。")


        # 创建一个唯一命名的文件夹来保存图片
        unique_folder_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(uuid.uuid4())[:8]
        upload_folder = StorageConst.UploadImgs + '/' + unique_folder_name

        # 创建文件夹
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        fs = FileSystemStorage(location=upload_folder)
        uploaded_file_paths = []
        for image in request.FILES.getlist('images'):
            filename = fs.save(image.name, image)
            uploaded_file_path = upload_folder + '/' + filename  # 这是文件在服务器上的实际路径
            # 将文件路径添加到列表中
            uploaded_file_paths.append(uploaded_file_path)

        # todo：数据库操作
        img_ply = Ply(video_path=uploaded_file_paths[0],
                      flag=1,  # flag为1，上传图片文件夹
                      )
        img_ply.save()

        return JsonResponse({'code': 200,
                             'msg': 'success upload images',
                             'data': uploaded_file_paths[0]},status=200)  # 返回第一张图片路径用于回显
    return JsonResponse({'code': 404, 'msg': 'failed to upload images', 'data': None})


# 查询图片模型信息
def list_img(request):
    img_plys = Ply.objects.filter(flag=1)
    results = [{'img_path': item.video_path,
                'upload_time': item.upload_time.strftime('%Y-%m-%d %H:%M'),
                'ply_path': item.ply_path,
                'ply_time': item.ply_time.strftime('%Y-%m-%d %H:%M') if item.ply_time is not None else item.ply_time,
                'is_finished': item.is_finished
                } for item in img_plys]

    return JsonResponse({'code': 200,
                         'msg': 'success search img_models',
                         'data': results})


# 查询视频模型信息
def list_video(request):
    video_plys = Ply.objects.filter(flag=0)
    results = [{'img_path': item.video_path,
                'upload_time': item.upload_time.strftime('%Y-%m-%d %H:%M'),
                'ply_path': item.ply_path,
                'ply_time': item.ply_time.strftime('%Y-%m-%d %H:%M') if item.ply_time is not None else item.ply_time,
                'is_finished': item.is_finished
                } for item in video_plys]

    return JsonResponse({'code': 200,
                         'msg': 'success search video_models',
                         'data': results})


"""个人页，返回个人信息以及个人模型信息"""
@jwt_required
def my_view(request):
    user = User.objects.get(id = request.user_id)
    plys = Ply.objects.filter(owner = user)
    response_data = {  
        'code': 200,  
        'msg': "success request",  
        'data': {  
            'nickname': user.nickname,
            'avator': user.avatar,
            'signature': user.signature,
            'plys': []
        }  
    } 
    for item in plys:
        ply_data = {
                'img_path': item.video_path,
                'upload_time': item.upload_time.strftime('%Y-%m-%d %H:%M'),
                'ply_path': item.ply_path,
                'ply_time': item.ply_time.strftime('%Y-%m-%d %H:%M') if item.ply_time is not None else item.ply_time,
                'is_finished': item.is_finished
            }
        response_data['data']['records'].append(ply_data) 
    return JsonResponse(response_data)