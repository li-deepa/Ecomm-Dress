# Generated by Django 4.2.2 on 2023-06-13 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0018_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='wislist.jpg', null=True, upload_to=''),
        ),
    ]