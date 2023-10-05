from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name='main'),
    path('alert/<str:alert_message>', views.alert_view, name='alert'),
  
    # 로그인/아웃, 회원가입 기능 관련
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('social_login_view/', views.social_login_view, name='social_login'),
  
  
    # 게시글 작성/수정, 검색 관련
    path('write/', views.write, name='write'),
    path('create_item/', views.create_item, name='create_item'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('search/', views.search, name='search'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:post_id>/', views.trade_post, name='trade_post'),
  
  
    # 지역 인증 관련
    path('location/', views.location, name='location'),
    path('set_region/', views.set_region, name='set_region'),
    path('set_region_certification/', views.set_region_certification, name='set_certification'),
    path('regionshop/', views.region_shop, name='region_shop'),
    path('regionshop/<str:category>', views.region_shop, name ='region_shop_category'),
    path('region_registration/', views.region_shop_registration, name='region_registration'),
    path('region_shop_detail/<int:shop_id>', views.region_shop_detail_view, name='region_shop_detail'),
  
  
    # 채팅 관련
    path('chat/', views.chat, name='chat'),
    path("chat_index", views.index, name='index'),  
    path('chat_index/<int:pk>/', views.chat_room, name='chat_room'),
    path('create_or_join_chat/<int:pk>/', views.create_or_join_chat, name='create_or_join_chat'),
    path('get_latest_chat/', views.get_latest_chat_no_pk, name='get_latest_chat_no_pk'),
    path('get_latest_chat/<int:pk>/', views.get_latest_chat, name='get_latest_chat'),
    # path("chat_index", views.index, name='index'),  
    # path('chat_index/<int:pk>/', views.chat_room, name='chat_room'),
    # path('create_or_join_chat/<int:pk>/', views.create_or_join_chat, name='create_or_join_chat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)