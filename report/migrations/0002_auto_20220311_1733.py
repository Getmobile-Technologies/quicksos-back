# Generated by Django 3.0 on 2022-03-11 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='image_url1',
            field=models.URLField(blank=True, null=True),
        ),
    ]