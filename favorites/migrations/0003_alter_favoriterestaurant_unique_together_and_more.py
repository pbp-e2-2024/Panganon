# Generated by Django 5.1.2 on 2024-12-22 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_remove_user_last_login'),
        ('favorites', '0002_alter_favoriterestaurant_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoriterestaurant',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='favoriterestaurant',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='favoriterestaurant',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='favoriterestaurant',
            name='added_at',
        ),
    ]
