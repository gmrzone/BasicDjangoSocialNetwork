# Generated by Django 3.1.3 on 2020-11-30 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_followintermidiary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followintermidiary',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
