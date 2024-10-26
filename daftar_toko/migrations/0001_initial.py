# Generated by Django 5.1.2 on 2024-10-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Makanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rating', models.FloatField()),
                ('rating_amount', models.IntegerField()),
                ('price_range', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField()),
                ('opening_hours', models.JSONField()),
                ('services', models.JSONField()),
                ('links', models.URLField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]