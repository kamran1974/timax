# Generated by Django 5.1 on 2024-12-20 20:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inout', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='device_id',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='شناسه دستگاه'),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='work_logs', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
