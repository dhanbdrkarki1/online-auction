# Generated by Django 4.2.9 on 2024-11-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0036_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-16T06:13:52.610030+00:00'),
        ),
    ]
