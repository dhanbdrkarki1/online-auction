# Generated by Django 4.2.9 on 2024-11-07 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lot', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.PositiveIntegerField()),
                ('transaction_time', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('Esewa', 'Esewa'), ('Khalti', 'Khalti')], default='', max_length=20)),
                ('status', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('lot', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='lot.lot')),
            ],
        ),
    ]
