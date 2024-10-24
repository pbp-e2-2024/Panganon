# Generated by Django 5.1.2 on 2024-10-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], max_length=8)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/')),
            ],
        ),
    ]
