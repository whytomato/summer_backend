# Generated by Django 4.2.4 on 2023-08-28 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '__first__'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(max_length=512, null=True)),
                ('isInvited', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('publisher', models.CharField(default='System', max_length=64)),
                ('invitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.invitation')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'user_message',
            },
        ),
    ]
