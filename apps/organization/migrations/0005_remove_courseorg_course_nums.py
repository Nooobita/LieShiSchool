# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-23 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='course_nums',
        ),
    ]
