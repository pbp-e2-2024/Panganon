# Generated by Django 5.1.2 on 2024-10-26 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0006_remove_recipe_user_recipe_profile_alter_recipe_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='about_me.userprofile'),
            preserve_default=False,
        ),
    ]