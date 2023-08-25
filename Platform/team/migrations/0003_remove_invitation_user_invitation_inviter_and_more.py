# Generated by Django 4.2.4 on 2023-08-25 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_user_truename_user_realname'),
        ('team', '0002_invitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='user',
        ),
        migrations.AddField(
            model_name='invitation',
            name='inviter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitations_sent', to='user.user'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitations_received', to='user.user'),
        ),
    ]