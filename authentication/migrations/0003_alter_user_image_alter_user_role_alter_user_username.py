# Generated by Django 5.1 on 2024-10-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], max_length=8),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
