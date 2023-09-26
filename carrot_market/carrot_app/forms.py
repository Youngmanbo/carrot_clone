from django import forms
from .models import Item

class ItemPost(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'price', 'content', 'sale_place']