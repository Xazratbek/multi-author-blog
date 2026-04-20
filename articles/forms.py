import json
from django import forms
from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from categories.models import Category, Tag
from .models import Article


class ArticleForm(ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'article-select w-full max-w-full'}),
        required=False,
        label='Teglar',
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Maqola sarlavhasi'}),
            'content': CKEditor5Widget(config_name='extends'),
            'category': forms.Select(
                attrs={'class': 'article-select w-full max-w-full'}
            ),
        }
        labels = {
            'title': 'Sarlavha',
            'content': 'Matn',
            'category': 'Kategoriya',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['category'].required = False
        self.fields['category'].empty_label = 'Kategoriya tanlang'

class ArticleAdminForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='extends'),
        }
