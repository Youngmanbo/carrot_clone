from django.urls import path
from . import views

app_name = 'dangun_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('location/', views.location, name='location'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_certification')
]