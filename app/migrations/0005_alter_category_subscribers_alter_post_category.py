# Generated by Django 5.0.4 on 2024-06-10 13:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_post_subscribers_remove_postcategory_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(related_name='posts', through='app.Subscribe', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(related_name='categories', through='app.PostCategory', to='app.category'),
        ),
    ]
