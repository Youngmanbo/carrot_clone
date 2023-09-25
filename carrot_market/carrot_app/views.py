from django.shortcuts import render
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

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')