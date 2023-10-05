from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
import json
import os
import requests
from pathlib import Path
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent

SECRETS_DIR = BASE_DIR / '.secrets'
secrets = json.load(open(os.path.join(SECRETS_DIR, 'secrets.json')))

# Create your models here.
class Item(models.Model):
    user_id             = models.ForeignKey(User, on_delete = models.CASCADE)
    title               = models.CharField(max_length = 50)
    content             = models.TextField()
    price               = models.CharField(max_length = 20)
    item_views          = models.PositiveIntegerField(default = 0)
    create_at           = models.DateTimeField(auto_now_add = True)
    dibs                = models.BooleanField(default = False)
    category            = models.CharField(max_length = 10)
    is_sold             = models.BooleanField(default = False)
    sale_place          = models.CharField(max_length = 30)
    region              = models.CharField(max_length = 30, default = None)
    
    class Meta:
        pass

class ItemImage(models.Model):
    item_id             = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_image          = models.ImageField(null = True, blank = True, upload_to = "images/item")

class ChatRoom(models.Model):
    room_number = models.AutoField(primary_key=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    latest_message_time = models.DateTimeField(null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='chat_rooms', null=True, blank=True)


    def __str__(self):
        return f'ChatRoom: {self.starter.username} and {self.receiver.username}'

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message: {self.author.username} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 새 메시지가 저장될 때마다 chatroom의 latest_message_time을 업데이트
        self.chatroom.latest_message_time = self.timestamp
        self.chatroom.save()
    
class UserProfile(models.Model):
    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    region               = models.CharField(max_length=100, null=True)
    region_certification = models.CharField(max_length=1, default='N')

    def __str__(self):
        return f'{self.user.username} Profile'

def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"images/thumbnail/{filename}"

class RegionShop(models.Model):
    # category 테이블  라디오버튼 처리
    CATEGORY_CHOICE = [
        ('all', '전체'),
        ('restaurant', '식당'),
        ('cafe', '카페'),
        ('move', '이사/용달'),
        ('beauty', '뷰티/미용'),
        ('health', '헬스/필라테스/요가')
    ]
    shopname              = models.CharField(max_length=50)
    address               = models.CharField(max_length=200, null=True)
    shopinfo              = models.TextField()
    thumnail              = models.ImageField(upload_to=image_upload_to, height_field=None, width_field=None, null=True, blank=True)
    neighborhood          = models.CharField(max_length=50, blank=True, null=True)
    category              = models.CharField(max_length=50, choices=CATEGORY_CHOICE, blank=True)
    
@receiver(pre_save, sender=RegionShop)
def extract_neighborhood(sender, instance, **kwargs):
    if instance.address:
        # 주소가 있을 경우 동네 정보를 추출하여 저장
        keyword = instance.address
        url = 'https://dapi.kakao.com/v2/local/search/address.json?&query='+keyword
        REST_API_KEY = secrets['KAKAO_API']
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            instance.neighborhood = data['documents'][0]['address']['region_3depth_name']
        else:
            print(f'Request failed with status: {response.status_code}')
            print(response.text)

def image_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"images/{filename}"
class RegionShopImages(models.Model):
    shop_id               = models.ForeignKey(RegionShop, on_delete=models.CASCADE, related_name='image')
    image                 = models.ImageField(upload_to=image_upload, height_field=None, width_field=None, blank=True, null=True)
    
class RegionShopProductPrice(models.Model):
    region_shop_id        = models.ForeignKey(RegionShop, on_delete=models.CASCADE, related_name='price')
    product_name          = models.CharField(max_length=20)
    product_price         = models.CharField(max_length=20)
    option                = models.CharField(max_length=200) 