# Generated by Django 4.2.9 on 2024-11-16 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0044_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-16T08:15:40.925852+00:00'),
        ),
    ]