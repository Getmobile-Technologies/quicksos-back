# Generated by Django 3.0 on 2023-07-20 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20230217_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='nearest_busstop',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='traffic_situation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='message',
            name='emergency_code',
        ),
        migrations.AddField(
            model_name='message',
            name='emergency_code',
            field=models.ManyToManyField(related_name='emergency_codes', to='main.EmergencyCode'),
        ),
    ]