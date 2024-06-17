import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import SITE_URL

def send_message_of_signup(user,email):

    msg = EmailMultiAlternatives(
        subject=f'Регистрация на новостном портале',
        body=f'{user}, поздравляем с успешной регистрацией!',
        from_email='dimonsmile98@yandex.ru',
        to=[email],
    )
    msg.send()


def send_message_on_email(text, title, pk, subscribers_user, subscribers_emails, url_text):

    for user, email in zip(subscribers_user, subscribers_emails):
        html_content = render_to_string('send.html',
                                        {
            'user': user.username,
            'text': text,
            'title' : title,
            'link' : f'{SITE_URL}{url_text}{pk}'
        }
                                    )

        msg = EmailMultiAlternatives(
            subject=title,
            body=text[0:50],
            from_email='dimonsmile98@yandex.ru',
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()



def weekly_send_notify(posts, emails):
    for email in emails:
        html_content = render_to_string('weeklysend.html',
                                        {
                                            'posts': posts,
                                            'link': SITE_URL,
                                            'user' : email
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