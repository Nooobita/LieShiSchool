# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-23 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170122_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='touxiang/default.png', upload_to='touxiang/%Y/%m'),
        ),
    ]
