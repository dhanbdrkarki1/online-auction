# Generated by Django 4.2.9 on 2024-11-11 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0022_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-11T07:13:52.468057+00:00'),
        ),
    ]
