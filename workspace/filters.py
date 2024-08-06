import django_filters

from news.models import Category, News


class NewsFilter(django_filters.FilterSet):


    categories = django_filters.ModelMultipleChoiceFilter(
        field_name='category', 
        queryset=Category.objects.all(),
        label='Категории'
    )
    date = django_filters.DateFromToRangeFilter()
    

    class Meta:
        model = News
        fields = ('tags', 'is_published', 'author')