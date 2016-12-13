# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step1', '0002_act'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='act',
            name='partner',
        ),
        migrations.AddField(
            model_name='act',
            name='partner',
            field=models.ManyToManyField(to='step1.User'),
        ),
    ]
