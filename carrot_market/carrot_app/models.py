from django.db import models
from django.contrib.auth.models import User

# Create your models here.

    
class Item(models.Model):
    user_id             = models.ForeignKey(User, on_delete = models.CASCADE)
    title               = models.CharField(max_length = 50)
    content             = models.TextField()
    price               = models.CharField(max_length = 20)
    item_views          = models.IntegerField()
    create_at           = models.DateTimeField(auto_now_add = True)
    dibs                = models.BooleanField(default = False)
    category            = models.CharField(max_length = 10)
    is_sold             = models.BooleanField(default = False)
    sale_place          = models.CharField(max_length = 30)

class ItemImage(models.Model):
    item_id             = models.ForeignKey(Item, on_delete = models.CASCADE)
    item_image          = models.ImageField(null = True, blank = True, upload_to = "")

class ChattingRoom(models.Model):
    user_id             = models.ForeignKey(User, on_delete = models.CASCADE)
    item_id             = models.ForeignKey(Item, on_delete = models.CASCADE)
    create_at           = models.DateTimeField(auto_now_add = True) # 수정검토?

class Chatting(models.Model):
    chatting_room       = models.ForeignKey(ChattingRoom, on_delete = models.CASCADE)
    user_id             = models.ForeignKey(User, on_delete = models.CASCADE)
    message             = models.TextField()
    is_read             = models.BooleanField(default = False)
    create_at           = models.DateTimeField(auto_now = True)
    
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