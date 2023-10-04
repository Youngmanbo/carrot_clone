from django                 import forms
from django.forms           import ModelForm, inlineformset_factory
from . models               import RegionShop, RegionShopImages, RegionShopProductPrice, Item
from django.forms import modelformset_factory
# from .models import Post

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'class': 'login-input'}),
        label='아이디',
        label_suffix='', 
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요', 'class': 'login-input'}),
        label='비밀번호',
        label_suffix='', 
    )

class CustomRegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'class': 'login-input'}),
        label='아이디',
        label_suffix='', 
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요', 'class': 'login-input'}),
        label='비밀번호',
        label_suffix='', 
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 다시 입력해주세요', 'class': 'login-input'}),
        label='비밀번호 확인',
        label_suffix='', 
    )
    
class ItemPost(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'content', 'sale_place']
        
class RegionShopForm(ModelForm):
    class Meta:
        model = RegionShop
        fields =  '__all__'
        
        widgets = {
            'category': forms.RadioSelect(choices=RegionShop.CATEGORY_CHOICE),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 특정 값을 체크된 상태로 설정 (예: 'cafe')
        self.fields['category'].initial = 'all'
        self.fields['shopname'].widget.attrs['class'] = 'cyberpunk'
        self.fields['address'].widget.attrs['class'] = 'cyberpunk'
        self.fields['shopinfo'].widget.attrs['class'] = 'cyberpunk'
        self.fields['thumnail'].widget.attrs['class'] = 'cyberpunk2077 red'
        self.fields['neighborhood'].widget.attrs['class'] = 'cyberpunk'
        self.fields['category'].widget.attrs['class'] = 'cyberpunk'

class StyledProductForm(forms.ModelForm):
    class Meta:
        model = RegionShopProductPrice
        fields = ('product_name', 'product_price', 'option')
        labels = {
        'product_name':  'hellow',
        'product_price': '<h2>상품가격 : </h2>',
        'option': '<h2>옵션 : </h2>',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 각 필드에 클래스 추가
        self.fields['product_name'].widget.attrs['class'] = 'cyberpunk'
        self.fields['product_price'].widget.attrs['class'] = 'cyberpunk'
        self.fields['option'].widget.attrs['class'] = 'cyberpunk'

class StyledImageForm(forms.ModelForm):
    class Meta:
        model = RegionShopImages
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 각 필드에 클래스 추가
        self.fields['image'].widget.attrs['class'] = 'cyberpunk'
