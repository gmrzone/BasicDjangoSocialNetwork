# Generated by Django 3.1.3 on 2020-11-26 18:53

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='image',
            field=models.ImageField(upload_to=images.models.get_username),
        ),
        migrations.AlterField(
            model_name='imagepost',
            name='slug',
            field=models.SlugField(blank=True, unique_for_date='created'),
        ),
    ]
