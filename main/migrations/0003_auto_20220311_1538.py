# Generated by Django 3.0 on 2022-03-11 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_message_escalators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='escalators',
            field=models.ManyToManyField(blank=True, related_name='messages', to='main.Escalator'),
        ),
    ]
