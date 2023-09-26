from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Item,UserProfile

# Create your views here.
def main(request):
    return render(request, 'carrot_app/main.html')

def trade(request):
    try:
        item = Item.objects.filter(is_sold=False).order_by('-views')

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
            messages.success('동네인증이 필요합니다.')
            return redirect('location')
        
    except UserProfile.DoesNotExist:
        messages.success(request, '동네인증이 필요합니다.')
        return redirect('location')
    
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