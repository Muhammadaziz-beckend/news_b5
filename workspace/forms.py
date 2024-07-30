
from django import forms

from news.models import Category, News, Tag


class NewsForm(forms.Form):

    name = forms.CharField(label='Название', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Название',
    }))
    image = forms.ImageField(label='Изображение', required=False, widget=forms.FileInput(attrs={
         'class': 'form-control',
    }))
    category = forms.ModelChoiceField(
        label='Категория', 
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    tags = forms.ModelMultipleChoiceField(
        label='Теги',
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    content = forms.CharField(label='Контент', widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '5'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '5'}))
    author = forms.CharField(label='Автор', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Автор',
    }))
    is_published = forms.BooleanField(label='Публичность', widget=forms.CheckboxInput(attrs={'id': 'news_is_pub'}))
    

class NewsModelForm(forms.ModelForm):

    class Meta:
        model = News
        fields = (
            'name',
            'description',
            'content',
            'category',
            'tags',
            'image',
            'author',
            'is_published',
        )

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название',
            }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': '5'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'content': forms.Textarea(attrs={'class': 'form-control', 'cols': '5'}),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Автор',
            })
        }