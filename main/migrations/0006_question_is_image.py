# Generated by Django 3.0 on 2022-06-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20220615_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_image',
            field=models.BooleanField(default=False),
        ),
    ]