# Generated by Django 3.0 on 2022-10-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20221004_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='archive_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='date_archived',
            field=models.DateTimeField(null=True),
        ),
    ]
