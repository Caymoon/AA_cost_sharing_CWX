# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-13 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('step1', '0010_auto_20161213_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='fin',
            field=models.ManyToManyField(related_name='fin_acts', to='step1.User'),
        ),
    ]
