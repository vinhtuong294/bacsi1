# Generated by Django 4.2.16 on 2024-12-08 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("datlich", "0009_rate_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="usermodel",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="users/images/"),
        ),
    ]
