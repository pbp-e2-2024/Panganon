# Generated by Django 5.1.2 on 2024-10-26 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0004_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='steps',
            field=models.JSONField(),
        ),
    ]
