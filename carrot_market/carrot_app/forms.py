from django import forms
from django.forms import ModelForm
from . models import RegionShop, RegionShopImages, RegionShopProductPrice
from django.forms import inlineformset_factory


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
    
class RegionShopForm(ModelForm):
    class Meta:
        model = RegionShop
        fields =  '__all__'
