# Generated by Django 2.1.3 on 2018-12-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20181219_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='index_in_saga',
            field=models.IntegerField(default=1, verbose_name='Index in saga'),
        ),
    ]
