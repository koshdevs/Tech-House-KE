# Generated by Django 5.1.2 on 2024-11-01 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_storesales_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('terms', models.TextField(blank=True, null=True)),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('payment', models.TextField()),
                ('terms', models.TextField()),
                ('logo', models.ImageField(default='', upload_to='org_pics')),
            ],
            options={
                'verbose_name_plural': 'Org Details',
            },
        ),
        migrations.AlterField(
            model_name='storesales',
            name='status',
            field=models.CharField(choices=[('cart', 'cart'), ('ínvoiced', 'invoiced'), ('sold', 'sold'), ('returned', 'returned'), ('delivered', 'delivered')], max_length=200),
        ),
        migrations.CreateModel(
            name='StoreOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sales', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.storesales')),
            ],
        ),
    ]
