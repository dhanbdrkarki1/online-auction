# Generated by Django 4.2.9 on 2024-11-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0072_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-16T13:42:09.911920+00:00'),
        ),
    ]
