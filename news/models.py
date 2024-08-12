from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


def news_image_upload_to(instance, filename):
    return f'news_image/{instance.name}/{filename}'


def min_length_validator(value):

    if len(value) <= 3:
        raise ValidationError('Name should contsins more than 3 chracters')
    
    return value
    


class News(models.Model):

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    name = models.CharField(verbose_name='название', max_length=100, validators=[min_length_validator])
    image = models.ImageField(verbose_name='изображение', upload_to=news_image_upload_to)
    category = models.ForeignKey(
        'news.Category', on_delete=models.PROTECT, related_name='news', verbose_name='категория')
    tags = models.ManyToManyField('news.Tag', related_name='news', verbose_name='теги')
    description = models.CharField(verbose_name='описание', max_length=300)
    content = models.TextField(verbose_name='контент')
    date = models.DateTimeField(verbose_name='дата добавление', auto_now_add=True)
    views = models.IntegerField(verbose_name='просмотры', default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='news', verbose_name='автор')
    is_published = models.BooleanField(verbose_name='публичность', default=True)

    def __str__(self):
        return f'{self.name}'
    

class SocialMediaLink(models.Model):

    class Meta:
        verbose_name = 'доп. инфо'
        verbose_name_plural = 'доп. инфы'
    
    site_link = models.URLField(verbose_name='ссылка сайта', blank=True, null=True)
    instagram_link = models.URLField(verbose_name='ссылка instagrm', blank=True, null=True)
    x_link = models.URLField(verbose_name='ссылка приложении x', blank=True, null=True)
    facebook_link = models.URLField(verbose_name='ссылка facebook', blank=True, null=True)
    telegram_link = models.URLField(verbose_name='ссылка telegram', blank=True, null=True)
    news = models.OneToOneField('news.News', on_delete=models.CASCADE, related_name='link', verbose_name='новость')

    def __str__(self) -> str:
        return f'{self.news.name}'

    

class Category(models.Model):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField(verbose_name='название', max_length=100)

    def __str__(self):
        return f'{self.name}'
    

class Tag(models.Model):

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField(verbose_name='название', max_length=100)

    def __str__(self):
        return f'{self.name}'
    

# Create your models here.
