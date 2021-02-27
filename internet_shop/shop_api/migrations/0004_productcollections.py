# Generated by Django 3.1.4 on 2021-02-24 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0003_auto_20210224_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCollections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('products', models.ManyToManyField(related_name='product_collections', to='shop_api.Product')),
            ],
            options={
                'verbose_name': 'Подборка',
                'verbose_name_plural': 'Подборки',
            },
        ),
    ]
