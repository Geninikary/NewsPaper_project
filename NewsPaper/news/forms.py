from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'categories',
            'title_articles_news',
            'author',
            #'articles_or_news',
            'text_articles_news'
        ]
        widgets = {
            'title_articles_news': forms.Textarea(attrs={'class': 'form-text', 'cols': 50, 'rows': 1}),
            'text_articles_news': forms.Textarea(attrs={'class': 'form-text', 'cols': 80, 'rows': 15})
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title_article_news')
        text = cleaned_data.get('text_articles_news')
        if title == text:
            raise ValidationError(
                'Название не олжно быть идентично тексту'
            )
        return cleaned_data


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
