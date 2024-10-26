# Generated by Django 5.1.2 on 2024-10-25 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about_me', '0003_delete_recipe'),
        ('authentication', '0003_alter_user_image_alter_user_role_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=100)),
                ('ingredients', models.TextField()),
                ('steps', models.TextField()),
                ('image', models.ImageField(upload_to='recipes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
        ),
    ]