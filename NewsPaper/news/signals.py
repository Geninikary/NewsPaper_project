from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_notifications(preview, pk, title_articles_news, subscribers):
    html_content = render_to_string(
        'send_email_create_post_cat.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title_articles_news,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notive_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()
        subscribers_email = []

        for cat in categories:
            subscribers = cat.subscribes.all()
            subscribers_email += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title_articles_news, subscribers_email)
