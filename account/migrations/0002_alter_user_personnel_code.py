# Generated by Django 5.1 on 2024-12-20 20:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personnel_code',
            field=models.CharField(default=uuid.uuid4, max_length=128, unique=True, verbose_name='کد پرسنلی'),
        ),
    ]
