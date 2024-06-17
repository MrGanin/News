from datetime import date
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from .tasks import send_message_on_email


@receiver(signal=pre_save, sender=Post)
def limits_posts(sender, instance, **kwargs):
    user = instance.author
    dtoday = date.today()
    len_sender_all_now = sender.objects.filter(date__date=dtoday, author_id=user).count()
    if len_sender_all_now >= 3:
        raise ValidationError('Публиковать больше 3-х статей в сутки, запрещено!')



# @receiver(signal=m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#         if kwargs['action'] == 'post_add':
#             category = instance.category.all()
#             emails = []
#             users = []
#             url_text = ''
#             for c in category:
#                 users = c.subscribers.all()
#                 emails += [u.email for u in c.subscribers.all()]
#
#             if instance.it_news == True:
#                 url_text = '/news/'
#             else:
#                 url_text = '/articles/'
#
#             send_message_on_email(instance.text, instance.title, instance.pk, users, emails, url_text)
#
