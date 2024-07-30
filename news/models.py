from django.db import models


class News(models.Model):

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    name = models.CharField(verbose_name='название', max_length=100)
    image = models.ImageField(verbose_name='изображение', upload_to='news_images/')
    category = models.ForeignKey(
        'news.Category', on_delete=models.PROTECT, related_name='news', verbose_name='категория')
    tags = models.ManyToManyField('news.Tag', related_name='news', verbose_name='теги')
    description = models.CharField(verbose_name='описание', max_length=300)
    content = models.TextField(verbose_name='контент')
    date = models.DateTimeField(verbose_name='дата добавление', auto_now_add=True)
    views = models.PositiveIntegerField(verbose_name='просмотры', default=0)
    author = models.CharField(verbose_name='автор', max_length=100, blank=True, null=True)
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
