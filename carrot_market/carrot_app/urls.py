from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('write/', views.write, name='write'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:post_id>/', views.trade_post, name='trade_post'),
]