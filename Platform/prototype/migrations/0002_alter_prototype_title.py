# Generated by Django 4.1 on 2023-08-30 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prototype", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prototype",
            name="title",
            field=models.CharField(max_length=64, null=True),
        ),
    ]