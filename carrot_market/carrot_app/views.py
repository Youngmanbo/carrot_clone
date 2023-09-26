from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Item,UserProfile,ItemImage
from .forms import ItemPost

# Create your views here.
def main(request):
    return render(request, 'carrot_app/main.html')

def chat(request):
    return render(request, 'carrot_app/chat.html')

def trade(request):
    try:
        item = Item.objects.filter(is_sold=False).order_by('-item_views')

    except:
        item = None

    content = {
        'posts': item
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

    content = {
        'post': item
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
            item.user_id = request.username
            item.save()
            return redirect('trade_post', post_id=item.post_id)
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
        images = ItemImage.objects.filter(item_id=id)

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


def login(request):
    return render(request, 'registration/login.html')

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

                return redirect('carrot_app:location')
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
        return redirect('carrot_app:location')