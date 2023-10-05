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
from django.utils.decorators        import method_decorator
from django.views                   import View

# Create your views here.
def main(request):
    try:
        item = Item.objects.filter(is_sold=False).order_by('-item_views')
    except:
        item = None

    content = {
        'posts': item,
    }
    return render(request, 'carrot_app/main.html', content)

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
            for img in request.FILES.getlist('item_image'):
                photo = ItemImage()
                photo.item_id_id = item.id
                photo.item_image = img
                photo.save()
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

    if request.method == "POST":
        item.title = request.POST['title']
        item.price = request.POST['price']
        item.content = request.POST['content']
        item.sale_place = request.POST['sale_place']
        item.save()
        for img in request.FILES.getlist('item_image'):
            photo = ItemImage()
            photo.item_id_id = item.id
            photo.item_image = img
            photo.save()
        return redirect('trade_post', post_id=id)
    
    content = {
        'post': item
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
    return redirect('main')

    
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

def region_shop(request, category=None):
    
    if category:
        queryset = RegionShop.objects.filter(category=category)
    else:
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
        form=StyledProductForm,
        extra=1,
    )
    
    # 레기온 이미지모델 폼셋 
    image_set = inlineformset_factory(
        RegionShop,
        RegionShopImages,
        form=StyledImageForm,
        extra=1,
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



def index(request): 
    return render(request, 'carrot_app/chat_index.html')


# 채팅방 열기
def chat_room(request, pk):
    user = request.user
    chat_room = get_object_or_404(ChatRoom, pk=pk)

    # 내 ID가 포함된 방만 가져오기
    chat_rooms = ChatRoom.objects.filter(
            Q(receiver_id=user) | Q(starter_id=user)
        ).order_by('-latest_message_time')  # 최신 메시지 시간을 기준으로 내림차순 정렬
    
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

    # 상대방 정보 가져오기
    if chat_room.receiver == user:
        opponent = chat_room.starter
    else:
        opponent = chat_room.receiver

    opponent_user = User.objects.get(pk=opponent.pk)


    # post의 상태 확인 및 처리
    if chat_room.item is None:
        seller = None
        post = None
    else:
        seller = chat_room.item.user_id
        post = chat_room.item

    return render(request, 'carrot_app/chat_room.html', {
        'chat_room': chat_room,
        'chat_room_data': chat_room_data,
        'room_name': chat_room.pk,
        'seller': seller,
        'post': post,
        'opponent': opponent_user,
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


# 가장 최근 채팅방 가져오기
@login_required
def get_latest_chat(request, pk):
    user = request.user
    # 1) 해당 pk인 채팅방 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat_with_pk = ChatRoom.objects.filter(
            Q(item_id=pk) &
            (Q(receiver=user) | Q(starter=user))
        ).latest('latest_message_time')
        return JsonResponse({'success': True, 'chat_room_id': latest_chat_with_pk.room_number})
    except ChatRoom.DoesNotExist:
        pass

    # 2) 위 경우가 없다면 내가 소속된 채팅방 전체 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user)
        ).latest('latest_message_time')
        return JsonResponse({'success': True, 'chat_room_id': latest_chat.room_number})

    # 3) 모두 없다면 현재 페이지로 리디렉션
    except ChatRoom.DoesNotExist:
        return redirect('alert', alert_message='진행중인 채팅이 없습니다.')
        
# nav/footer에서 채팅하기 눌렀을 때
@login_required
def get_latest_chat_no_pk(request):
    user = request.user
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user),
            latest_message_time__isnull=False
        ).latest('latest_message_time')
        return redirect('chat_room', pk=latest_chat.room_number)

    except ChatRoom.DoesNotExist:
        return redirect('alert', alert_message='진행중인 채팅이 없습니다.')
    
@method_decorator(login_required, name='dispatch')
class ConfirmDealView(View):
    def post(self, request, item_id):
        post = get_object_or_404(Item, pk=item_id)
        user = request.user

        previous_url = request.META.get('HTTP_REFERER')
        url_parts = previous_url.split('/')
        original_post_id = url_parts[-2] if url_parts[-1] == '' else url_parts[-1]

        chat_room = get_object_or_404(ChatRoom, room_number=original_post_id)


        if chat_room.starter == user:
            other_user = chat_room.receiver
        else:
            other_user = chat_room.starter

        if chat_room is None:
            messages.error(request, 'Chat room does not exist.')
            return redirect('carrot_app:trade')
        
        # buyer를 설정하고, product_sold를 Y로 설정
        post.buyer = chat_room.receiver if chat_room.starter == post.user else chat_room.starter
        post.product_sold = 'Y'
        post.save()
        
        # 거래가 확정되면 새로고침
        return redirect('carrot_app:chat_room', pk=chat_room.room_number)

      
 # social login
def social_login_view(request):
    return render(request, 'registration/login.html')
