from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.jwt import generate_jwt_token  # 生成jwt
from utils.decorators import jwt_required

from .models import User
# Create your views here.

"""登录"""
@csrf_exempt  # 不使用CSRF保护
def login_view(request):  
    if request.method == 'POST':  
        username = request.POST.get('username')  
        password = request.POST.get('password')  
        try:  
            user = User.objects.get(username=username)  
            # # TODO:优化密码验证的逻辑（比如使用哈希和比对）  
            # if user.check_password(password):  # 后期自定义check_password方法  
            if password == user.pwd: 
                token = generate_jwt_token(user)  
                return JsonResponse({'token': token})  
            else:  
                return JsonResponse({'error': 'Invalid credentials'}, status=400)  
        except User.DoesNotExist:  
            return JsonResponse({'error': 'User not found'}, status=400)  
    return JsonResponse({'error': 'Invalid request'}, status=400)




