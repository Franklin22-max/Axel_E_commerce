# Generated by Django 4.2.5 on 2023-09-21 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0004_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.CharField(default='', max_length=500),
        ),
    ]
