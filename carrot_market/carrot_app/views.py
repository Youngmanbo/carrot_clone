from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http                    import JsonResponse
from django.contrib.auth.forms      import UserCreationForm
from django.contrib                 import auth, messages
from django.contrib.auth.models     import User
from django.contrib.auth            import authenticate
from django.contrib.auth            import login as custom_login
from django.shortcuts               import render, redirect
from django.db.models               import Q
from .models                        import *
from .forms                         import *

# Create your views here.
def main(request):
    return render(request, 'carrot_app/main.html')

def trade(request):
    try:
        item = Item.objects.filter(is_sold=False).order_by('-item_views')
    except:
        item = None

    content = {
        'posts': item,
    }
    
    return render(request, 'carrot_app/trade.html', content)

def trade_post(request, post_id):
    item = Item.objects.get(id=post_id)

    if request.user.is_authenticated:
        if request.user != item.user_id:
            item.item_views += 1
            item.save()
    else:
        item.item_views += 1
        item.save()

    if request.method == "POST":
        if 'delete' in request.POST:
            if item:
                item.delete()
                return redirect('trade')

    content = {
        'post': item
    }

    return render(request, 'carrot_app/trade_post.html', content)

@login_required
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
    user_profile = UserProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = ItemPost(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user_id = request.user
            item.region = user_profile.region
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
            
                return redirect('login')
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
        print(region)

        if region:
            try:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.region = region
                user_profile.save()

                return redirect('location')
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
        return redirect('location')

def search(request):
    query = request.GET.get('search')
    
    if query:
        results = Item.objects.filter(Q(title__icontains=query) | Q(region__icontains=query))
    else:
        results = None

    content = {
        'posts': results
    }
    
    return render(request, 'carrot_app/search.html', content)

def region_shop(request):
    queryset = RegionShop.objects.all()
    context = {'data':queryset}
    
    return render(request, 'carrot_app/region_shop.html', context)

def region_shop_detail_view(request, shop_id):
    if request.method == 'GET':
        data = RegionShop.objects.get(id=shop_id)
        context = {'data':data}
    return render(request, 'carrot_app/region_shop_detail.html', context)

def region_shop_registration(request):
    
    # 레기온 샾 기본 폼
    f = RegionShopForm()
    
    # 래기온 프로덕트 프라이스 모델폼셋
    product_formset = inlineformset_factory(
        RegionShop,
        RegionShopProductPrice,
        fields = (
            'product_name',
            'product_price',
            'option'
        ),
        extra=2,
        can_delete=True,
    )
    
    # 레기온 이미지모델 폼셋 
    image_set = inlineformset_factory(
        RegionShop,
        RegionShopImages,
        fields = (
            'image',
        ),
        extra=2,
        can_delete=True
    )
    
    if request.method == "POST":
        form = RegionShopForm(request.POST, request.FILES)
        product_formset = product_formset(request.POST, instance=RegionShop())
        image_set = image_set(request.POST, request.FILES, instance=RegionShop())
        
        if form.is_valid() and product_formset.is_valid() and image_set.is_valid():
            region = form.save()
            p_instance = product_formset.save(commit=False)
            image_instance = image_set.save(commit=False)
            
            for instance in p_instance:
                instance.region_shop_id = region
                instance.save()
            
            for instance in image_instance:
                instance.shop_id = region
                instance.save()
            
            return redirect('main')
        else:
            return redirect('region_registration')
    
    context = {'formset':product_formset(instance=RegionShop()),
               'form':f, 
               'image_set':image_set(instance=RegionShop())
               }
    return render(request, 'carrot_app/region_shop_registration.html', context)

# 채팅테스트

def index(request): 
    return render(request, 'carrot_app/chat_index.html')


# 채팅방 열기
def chat_room(request, pk):
    user = request.user
    chat_room = get_object_or_404(ChatRoom, pk=pk)

    # 내 ID가 포함된 방만 가져오기
    chat_rooms = ChatRoom.objects.filter(Q(receiver_id=user) | Q(starter_id=user))

    # 각 채팅방의 최신 메시지를 가져오기
    chat_room_data = []
    for room in chat_rooms:
        latest_message = Message.objects.filter(chatroom=room).order_by('-timestamp').first()
        if latest_message:
            chat_room_data.append({
                'chat_room': room,
                'latest_message': latest_message.content,
                'timestamp': latest_message.timestamp,
            })


    # post의 상태 확인 및 처리
    if chat_room.item is None:
        seller = None
        item = None
    else:
        seller = chat_room.item.user_id
        item = chat_room.item

    return render(request, 'carrot_app/chat_room.html', {
        'chat_room': chat_room,
        'chat_room_data': chat_room_data,
        'room_name': chat_room.pk,
        'seller': seller,
        'item': item,
    })


# 채팅방 생성 또는 참여
def create_or_join_chat(request, pk):
    item = get_object_or_404(Item, pk=pk)
    user = request.user
    chat_room = None
    created = False

    # 채팅방이 이미 존재하는지 확인
    chat_rooms = ChatRoom.objects.filter(
        Q(starter=user, receiver=item.user_id, item=item) |
        Q(starter=item.user_id, receiver=user, item=item)
    )
    if chat_rooms.exists():
        chat_room = chat_rooms.first()
    else:
        # 채팅방이 존재하지 않는 경우, 새로운 채팅방 생성
        chat_room = ChatRoom(starter=user, receiver=item.user_id, item=item)
        chat_room.save()
        created = True

    return JsonResponse({'success': True, 'chat_room_id': chat_room.pk, 'created': created})
