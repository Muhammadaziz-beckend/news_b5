from django.contrib import admin
from news.models import News, Category, Tag, SocialMediaLink
from django.utils.safestring import mark_safe


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'category', 
        'date',
        'views',
        'author', 
        'is_published',
        'get_image', 
    )
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    search_fields = (
        'name', 
        'description', 
        'content', 
        'tags__name', 
        'category__name',
        'author__first_name',
        'author__last_name',
    )
    list_filter = ('tags', 'category', 'is_published', 'date', 'author')

    readonly_fields = (
        'views',
        'date',
        'get_full_image',
    )


    @admin.display(description='Изображение')
    def get_image(self, instance: News):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="100px">')
        return '-'
    
    @admin.display(description='Изображение')
    def get_full_image(self, instance: News):
        if instance.image:
            return mark_safe(f'<img src="{instance.image.url}" width="50%">')
        return '-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'news')
    list_display_links = ('id', 'news')
    list_filter = ('news',)
    search_fields = ('news__name', 'news__description', 'news__content')

# Register your models here.
