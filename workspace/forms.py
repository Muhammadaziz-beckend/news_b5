
from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from news.models import Category, News, Tag
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password



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
        }

    
class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form-control'}), 
        label='Имя пользователя'
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form-control'}),
    )


class RegisterForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True 
        self.fields['last_name'].required = True 
        self.fields['email'].required = True 


    password1 = forms.CharField(label='Придумайте пароль', validators=[validate_password], widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    # first_name = forms.CharField(required=True)


    class Meta:
        model = User
        # fields = '__all__'
        exclude = (
            'password', 
            'is_superuser', 
            'is_staff',
            'is_active',
            'user_permissions', 
            'groups', 
            'last_login', 
            'date_joined'
            )
        
        # labels = {
        #     'username': 'sdfsd'
        # }


        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            # last_name
        }
    
    
    def clean(self):
       
        cleaned_data = super().clean()
        
        password1 = cleaned_data.pop('password1', None)
        password2 = cleaned_data.pop('password2', None)

        # errors = {}

        # if password1 is None:
        #     errors['password1'] = ['Обязательное поле.']

        # if password2 is None:
        #     errors['password2'] = ['Обязательное поле.']

        # if len(errors) > 0:
        #     raise forms.ValidationError(errors)

        if (password1 is not None and password2 is not None) and password1 != password2:
            raise forms.ValidationError({'password2': ['The passwords dont\'t match.']})

        
        password = make_password(password1)
        cleaned_data.setdefault('password', password)

        return cleaned_data
       

class ChangeProfileForm(forms.ModelForm):


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }
    

class ChangePsswordForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user


    old_password = forms.CharField(
        label='Current paassword', 
        widget=forms.PasswordInput({'class': 'form-control'}),
        )
    new_password = forms.CharField(
        label='New paassword', 
        widget=forms.PasswordInput({'class': 'form-control'}),
        validators=[validate_password]
        )
    
    confirm_password = forms.CharField(
        label='Confirm paassword', 
        widget=forms.PasswordInput({'class': 'form-control'}),
        )
    

    def clean(self):

        cleaned_data = super().clean()

        errors = {}

        old_password = cleaned_data.get('old_password', None)
        new_password = cleaned_data.get('new_password', None)
        confirm_password = cleaned_data.get('confirm_password', None)

        if old_password:
            if not self.user.check_password(old_password):
                errors['old_password'] = ['The current password is incorrect']
       
        if (new_password is not None and confirm_password is not None) \
            and new_password != confirm_password:
            errors['confirm_password'] = ['The passwords dont\'t match.']


        if len(errors) > 0:
            raise forms.ValidationError(errors)

        return cleaned_data