# Generated by Django 3.1.1 on 2020-09-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20200925_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='/images/default_profile.png', upload_to='users/%Y/%m/%d/'),
        ),
    ]
