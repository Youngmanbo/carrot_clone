from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory

from .models import UserProfile, RegionShop, RegionShopProductPrice, RegionShopImages
from django.contrib.auth.decorators import login_required

from .forms import CustomLoginForm, RegionShopForm

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

def custom_login(request):
    # 이미 로그인한 경우
    if request.user.is_authenticated:
        return redirect('dangun_app:main')
    
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
                    login(request, user) # 로그인 처리 및 세션에 사용자 정보 저장
                    return redirect('dangun_app:main')  # 리다이렉션
        return render(request, 'registration/login.html', {'form': form}) #폼을 템플릿으로 전달

def register(request):
    return render(request, 'registration/register.html')

@login_required
def location(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.user)
        region = user_profile.region
    except UserProfile.DoesNotExist:
        region = None

    return render(request, 'carrot_app/location.html', {'region': region})

@login_required
def set_region(request):
    if request.method == "POST":
        region = request.POST.get('region-setting')

        if region:
            try:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.region = region
                user_profile.save()

                return redirect('dangun_app:location')
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "Region cannot be empty"})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

# 지역인증 완료
@login_required
def set_region_certification(request):
    if request.method == "POST":
        request.user.profile.region_certification = 'Y'
        request.user.profile.save()
        messages.success(request, "인증되었습니다")
        return redirect('dangun_app:location')
    
def chat():
    pass

def logout():
    pass

def region_shop(request):
    form = RegionShopForm()
    return render(request, 'carrot_app/region_shop.html', {'form':form})

def region_shop_registration(request):
    f = RegionShopForm()
    form_set = inlineformset_factory(
    RegionShop,
    RegionShopProductPrice,
    fields = (
        'product_name',
        'product_price',
    ),
    extra=2,
    can_delete=True,
    )
    context = {'formset':form_set(instance=RegionShop())}
    return render(request, 'carrot_app/region_shop_registration.html', context)