# Generated by Django 3.1.5 on 2021-02-18 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0011_auto_20210217_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='Цена'),
        ),
    ]
