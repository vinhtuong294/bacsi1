# Generated by Django 5.1.1 on 2024-12-07 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datlich', '0005_alter_schedule_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
