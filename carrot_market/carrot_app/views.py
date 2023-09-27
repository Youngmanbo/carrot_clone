from django.shortcuts               import render, redirect
from django.contrib.auth.decorators import login_required
from django.http                    import JsonResponse
from django.contrib.auth.forms      import UserCreationForm
from django.contrib                 import auth, messages
from django.contrib.auth.models     import User
from django.contrib.auth            import authenticate
from django.contrib.auth            import login as custom_login
from django.shortcuts               import render, redirect
from .models                        import *
from .forms                         import *

# Create your views here.
def main(request):
    return render(request, 'carrot_app/main.html')

def trade(request):
    try:
        item = Item.objects.filter(is_sold=False).order_by('-item_views')
        users = UserProfile.objects.all()
    except:
        item = None
        users = None

    content = {
        'posts': item,
        'users': users
    }
    
    return render(request, 'carrot_app/trade.html', content)

def trade_post(request, post_id):
    item = Item.objects.get(id=post_id)
    users = UserProfile.objects.all()

    if request.user.is_authenticated:
        if request.user != item.user_id:
            item.item_views += 1
            item.save()
    else:
        item.item_views += 1
        item.save()

    content = {
        'post': item,
        'users': users
    }

    return render(request, 'carrot_app/trade_post.html', content)

# @login_required
def write(request):
    try:
        user_profile = UserProfile.objects.get(user = request.user)

        if user_profile.region_certification == 'Y':
            return render(request, 'carrot_app/write.html')
        else:
            messages.success(request, '동네인증이 필요합니다.')
            return redirect('location')
        
    except UserProfile.DoesNotExist:
        messages.success(request, '동네인증이 필요합니다.')
        return redirect('location')

def create_item(request):
    if request.method == 'POST':
        form = ItemPost(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user
            item.save()
            return redirect('trade_post', post_id=item.id)
    else:
        form = ItemPost()
    
    content = {
        'form': ItemPost()
    }

    return render(request, 'carrot_app/trade_post.html', content)

def edit(request, id):
    item = Item.objects.get(id=id)
    
    if item:
        item.content = item.content.strip()
        # images = ItemImage.objects.filter(item_id=id)

    if request.method == "POST":
        item.title = request.POST['title']
        item.price = request.POST['price']
        item.content = request.POST['content']
        item.sale_place = request.POST['sale_place']
        # if 'item_image' in request.FILES:
        #     images.item_image = request.FILES['item_image']
        item.save()
        return redirect('trade_post', post_id=id)
    
    content = {
        'post': item,
        # 'item_image': images.item_image
    }
    return render(request, 'carrot_app/write.html', content)


# 로그인 화면
def login(request):
    # 이미 로그인한 경우
    if request.user.is_authenticated:
        return redirect('main')
    
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
    auth.logout(request)
    return render(request, 'carrot_app/main.html')

    
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

def search():
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