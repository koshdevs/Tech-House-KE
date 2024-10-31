# Generated by Django 5.1 on 2024-10-28 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_alter_productimages_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbuild',
            name='stage',
            field=models.CharField(choices=[('in-stock', 'in-stock'), ('sold', 'sold'), ('returned', 'returned')], default='in-stock', max_length=100),
        ),
    ]