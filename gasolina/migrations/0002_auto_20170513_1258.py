# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-13 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gasolina', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotstate',
            name='litres',
            field=models.FloatField(default=0, verbose_name='Litres'),
        ),
    ]
