# Generated by Django 3.1.4 on 2021-02-24 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0002_product_product_collection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_collection',
        ),
        migrations.DeleteModel(
            name='ProductCollections',
        ),
    ]
