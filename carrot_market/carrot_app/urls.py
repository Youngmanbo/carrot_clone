from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('location/', views.location, name='location'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_certification'),
    path('write/', views.write, name='write'),
    path('create_item/', views.create_item, name='create_item'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('chat/', views.chat, name='chat'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:post_id>/', views.trade_post, name='trade_post'),
    path('login/', views.login, name='login'),
#   path('logout/', views.logout, name='logout'),
    path('main/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('regionshop/', views.region_shop, name='region_shop'),
    path('region_registration', views.region_shop_registration, name='region_registration'),

    # 채팅
    path("chat_index", views.index, name='index'),  
    path('chat_index/<int:pk>/', views.chat_room, name='chat_room'),
    path('create_or_join_chat/<int:pk>/', views.create_or_join_chat, name='create_or_join_chat'),

]