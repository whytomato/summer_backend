# Generated by Django 4.2.4 on 2023-08-31 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="fileName",
            field=models.CharField(max_length=1024, null=True),
        ),
    ]