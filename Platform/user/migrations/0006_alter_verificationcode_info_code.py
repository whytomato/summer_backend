# Generated by Django 4.2.4 on 2023-08-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_verificationcode_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationcode_info',
            name='code',
            field=models.CharField(max_length=6, null=True, verbose_name='code'),
        ),
    ]
