import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import SITE_URL
from app.models import Post


@shared_task
def task_send_message():
    post = Post.objects.last()
    subscribers_emails = post.category.values_list('subscribers__email', flat=True)
    subscribers_user = post.category.values_list('subscribers__username', flat=True)
    url_text = '/news/' if post.it_news == True else '/articles/'

    for user, email in zip(subscribers_user, subscribers_emails):
        html_content = render_to_string('send.html',
                                        {
            'user': user,
            'text': post.text,
            'title' : post.title,
            'link' : f'{SITE_URL}{url_text}{post.pk}'
        }
                                    )

        msg = EmailMultiAlternatives(
            subject=post.title,
            body=post.text[0:50],
            from_email='dimonsmile98@yandex.ru',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()




@shared_task
def task_weekly_send():
    last_week = datetime.datetime.now() - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    emails = set(posts.values_list('category__subscribers__email', flat=True))

    for email in emails:
        html_content = render_to_string('weeklysend.html',
                                        {
                                            'posts': posts,
                                            'link': SITE_URL,
                                            'user': email
                                        }
                                        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email='dimonsmile98@yandex.ru',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()