# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-07-20 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_big',
            field=models.URLField(null=True),
        ),
    ]
