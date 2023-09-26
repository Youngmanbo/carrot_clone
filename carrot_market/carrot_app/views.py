from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.http                    import JsonResponse
# 가입 화면
from django.contrib.auth.models     import User
from django.contrib.auth            import authenticate, login
from django.shortcuts               import render, redirect
from .forms                         import CustomLoginForm, CustomRegistrationForm
from django.contrib.auth            import login as custom_login

# from .models import Post,UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def main(request):
    return render(request, 'carrot_app/main.html')

# @login_required
def write(request):
    try:
        pass
    except:
        pass
    return render(request, 'carrot_app/write.html')

def trade(request):
    return render(request, 'carrot_app/trade.html')

def trade_post(request):
    return render(request, 'carrot_app/trade_post.html')

# 로그인 화면
def login(request):
    # 이미 로그인한 경우
    if request.user.is_authenticated:
        return redirect('carrot_app:main')
    
    else:
        form = CustomLoginForm(data=request.POST or None)
        if request.method == "POST":

            # 입력정보가 유효한 경우 각 필드 정보 가져옴
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # 위 정보로 사용자 인증(authenticate사용하여 superuser로 로그인 가능)
                user = authenticate(request, username=username, password=password)

                # 로그인이 성공한 경우
                if user is not None:
                    custom_login(request, user) # 로그인 처리 및 세션에 사용자 정보 저장
                    return redirect('main')  # 리다이렉션
        return render(request, 'registration/login.html', {'form': form}) #폼을 템플릿으로 전달

def register(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            error_message = "이미 존재하는 아이디입니다."
        elif form.is_valid():
            
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            # 비밀번호 일치 여부를 확인
            if password1 == password2:
                # 새로운 유저를 생성
                user = User.objects.create_user(username=username, password=password1)
                
                # 유저를 로그인 상태로 만듦
                custom_login(request, user)
            
                return redirect('carrot_app:login')
            else:
                form.add_error('password2', '비밀번호가 일치하지 않습니다.')
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form, 'error_message': error_message})

# 로그인 후 main 구현 확인을 위해 임시로 작성해둔 함수 (chat, logout)
@login_required
def chat(request):
    return render(request, 'carrot_app/chat.html')

@login_required
def logout(request):
    return render(request, 'carrot_app/main.html')

    
# @login_required
# def location(request):
#     try:
#         user_profile = UserProfile.objects.get(user_id=request.user)
#         region = user_profile.region
#     except UserProfile.DoesNotExist:
#         region = None

#     return render(request, 'carrot_app/location.html', {'region': region})

# @login_required
# def set_region(request):
#     if request.method == "POST":
#         region = request.POST.get('region-setting')

#         if region:
#             try:
#                 user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#                 user_profile.region = region
#                 user_profile.save()

#                 return redirect('carrot_app:location')
#             except Exception as e:
#                 return JsonResponse({"status": "error", "message": str(e)})
#         else:
#             return JsonResponse({"status": "error", "message": "Region cannot be empty"})
#     else:
#         return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

# # 지역인증 완료
# @login_required
# def set_region_certification(request):
#     if request.method == "POST":
#         request.user.profile.region_certification = 'Y'
#         request.user.profile.save()
#         messages.success(request, "인증되었습니다")
#         return redirect('carrot_app:location')