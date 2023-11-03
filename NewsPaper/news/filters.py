from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from django_filters import DateTimeFilter
from django.forms import DateInput
from .models import Post, User


class PostFilter(FilterSet):

    search_author = ModelChoiceFilter(
        field_name='author__user',
        queryset=User.objects.all(),
        label='Автор',
        empty_label='Все авторы',
    )

    search_title = CharFilter(
        field_name='title_articles_news',
        label='Заголовок',
        lookup_expr='icontains'
    )

    search_time = DateTimeFilter(
         field_name='time_create',
         label='Дата',
         lookup_expr='date__gte',
         widget=DateInput(attrs={'type': 'date'})
    )

