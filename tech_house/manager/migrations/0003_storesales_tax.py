# Generated by Django 5.1 on 2024-10-30 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_alter_storesales_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='storesales',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=16.0, max_digits=10),
        ),
    ]