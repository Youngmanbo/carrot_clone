from django.db import models
from django.contrib.auth.models import User

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

class ItemImage(models.Model):
    item_id             = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_image          = models.ImageField(null = True, blank = True, upload_to = "")

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
    
    
class RegionShop(models.Model):
    shopname              = models.CharField(max_length=50)
    address               = models.CharField(max_length=200, null=True)
    shopinfo              = models.CharField(max_length=200)
    
class RegionShopImages(models.Model):
    shop_id               = models.ForeignKey(RegionShop, on_delete=models.CASCADE)
    image                 = models.ImageField(upload_to='', height_field=None, width_field=None)
    
class RegionShopProductPrice(models.Model):
    region_shop_id               = models.ForeignKey(RegionShop, on_delete=models.CASCADE)
    product_name          = models.CharField(max_length=20)
    product_price         = models.IntegerField()
    option                = models.CharField(max_length=200)