# Generated by Django 4.2.9 on 2024-11-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0080_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-16T14:57:36.200739+00:00'),
        ),
    ]