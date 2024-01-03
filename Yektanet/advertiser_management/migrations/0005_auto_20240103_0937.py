# Generated by Django 3.1.4 on 2024-01-03 09:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0004_auto_20240102_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='click',
            name='view_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='view',
            name='view_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
