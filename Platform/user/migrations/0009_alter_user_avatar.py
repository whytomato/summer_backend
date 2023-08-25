# Generated by Django 4.2.4 on 2023-08-25 16:26

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.User.user_directory_path, verbose_name='avatar'),
        ),
    ]