# Generated by Django 3.0 on 2022-07-01 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedcase',
            name='arrived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assignedcase',
            name='responded',
            field=models.BooleanField(default=False),
        ),
    ]
