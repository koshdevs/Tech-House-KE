# Generated by Django 5.1 on 2024-10-28 01:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecommerce', '0003_alter_productimages_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now=True)),
                ('status', models.CharField(choices=[('sold', 'sold'), ('returned', 'returned'), ('delivered', 'delivered')], max_length=200)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productbuild')),
            ],
            options={
                'verbose_name_plural': 'Store Sales',
            },
        ),
    ]