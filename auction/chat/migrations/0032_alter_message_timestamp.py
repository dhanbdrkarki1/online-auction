# Generated by Django 4.2.9 on 2024-11-16 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0031_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-16T04:53:54.566501+00:00'),
        ),
    ]