# Generated by Django 3.1.5 on 2021-02-16 13:19

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop_api', '0008_auto_20210216_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMethods',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_api.usermethods', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='shop_api.usermethods', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='review',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_api.usermethods', verbose_name='Автор'),
        ),
    ]