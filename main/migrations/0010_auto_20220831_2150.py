# Generated by Django 3.0 on 2022-08-31 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_emergencycode_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_emergency',
        ),
        migrations.AddField(
            model_name='message',
            name='category',
            field=models.CharField(blank=True, choices=[('emergency', 'Emergency'), ('non_emergency', 'Non-Emergency'), ('hoax', 'Hoax')], max_length=100, null=True),
        ),
    ]
