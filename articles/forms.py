from django import forms
from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title','content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Maqola sarlavhasi'}),
            'content': CKEditor5Widget(config_name='extends'),
        }


class ArticleAdminForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='extends'),
        }
