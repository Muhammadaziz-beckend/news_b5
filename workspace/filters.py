import django_filters
import django_filters.widgets
from django import forms
from django.contrib.auth.models import User
from news.models import Category, News, Tag


class NewsFilter(django_filters.FilterSet):

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), widget=forms.Select(attrs={"class": "form-select"})
    )

    tags = django_filters.ModelChoiceFilter(
        queryset=Tag.objects.all(), widget=forms.Select(attrs={"class": "form-select"})
    )

    date = django_filters.DateRangeFilter(
        field_name="date",
        empty_label="Выберите вариант",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = News
        fields = (
            "author",
            "category",
            "tags",
        )


class WorkspaceFilter(django_filters.FilterSet):

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )

    tags = django_filters.ModelChoiceFilter(
        queryset=Tag.objects.all(), 
        widget=forms.Select(attrs={"class": "form-select"})
    )

    date = django_filters.DateRangeFilter(
        field_name="date",
        empty_label="Выберите вариант",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    is_published = django_filters.BooleanFilter(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    class Meta:
        model = News
        fields = (
            "category",
            "tags",
            "date",
            "is_published",
        )
