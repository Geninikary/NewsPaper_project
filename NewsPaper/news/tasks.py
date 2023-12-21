from celery import shared_task
from .models import Category, Post
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta


@shared_task
def send_mail_to_user(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    subscribers_email = []
    for category in categories:
        subscriber = category.subscribes.all()
        subscribers_email += [s.email for s in subscriber]
    html_content = render_to_string(
        'send_email_from_tasks.html',
        {
            'text': Post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
         }
    )
    msg = EmailMultiAlternatives(
        subject=post.title_articles_news,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print()
    print('------------------------------------------------------------')
    print("I finish it!")
    print('------------------------------------------------------------')


@shared_task
def send_mail_every_monday_8am(pk):
    today = datetime.now()
    week = today - timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=week)

    categories = set(posts.values_list('categories__name_of_category', flat=True))
    subscribers_email = set(Category.objects.filter(name_of_category__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'email_posts_for_the_week.html',
        {
            'posts': posts,
            'link': f'{settings.SITE_URL}/news/'
        }
    )
    msg = EmailMultiAlternatives(
        subject=posts.title_articles_news,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('__________________________')
    print('Look, I finish it there.')
    print('--------------------------')