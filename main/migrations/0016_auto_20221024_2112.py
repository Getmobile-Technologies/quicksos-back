# Generated by Django 3.0 on 2022-10-24 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20221020_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='landmark',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]