# Generated by Django 4.2.2 on 2023-06-13 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0016_customer_order_orderitem_shippingaddress_delete_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]