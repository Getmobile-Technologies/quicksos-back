# Generated by Django 3.0 on 2022-08-22 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220614_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firebase_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
