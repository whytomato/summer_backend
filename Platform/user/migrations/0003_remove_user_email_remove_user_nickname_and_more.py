# Generated by Django 4.2.4 on 2023-08-24 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_nickname_user_truename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='user',
            name='truename',
        ),
    ]
