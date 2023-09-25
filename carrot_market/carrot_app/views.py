from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    return render(request, "main.html")

def location(request):
    return render(request, 'carrot_app/location.html')

def set_region(request):
    region = request.POST['region-setting']
    return render(request, 'carrot_app/location.html', {'region':region})

def set_region_certification(request):
    if request.method == 'POST':
        print(request.POST)
    return redirect('dangun_app:location')