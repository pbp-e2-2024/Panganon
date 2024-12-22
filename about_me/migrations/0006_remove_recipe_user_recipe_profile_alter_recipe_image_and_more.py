# Generated by Django 5.1.2 on 2024-10-26 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0005_alter_recipe_ingredients_alter_recipe_steps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='user',
        ),
        migrations.AddField(
            model_name='recipe',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='about_me.userprofile'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='steps',
            field=models.TextField(),
        ),
    ]
