from django.urls import path
from . import views

app_name = 'dangun_app'

urlpatterns = [
    path('', views.main, name='main'),
    path('location/', views.location, name='location'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_certification'),
    path('write/', views.write, name='write'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:post_id>/', views.trade_post, name='trade_post'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('chat/', views.chat, name='chat'),
    path('regionshop/', views.region_shop, name='region_shop'),
    path('region_registration', views.region_shop_registration, name='region_registration'),
]