# Generated by Django 4.2.2 on 2023-06-11 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0008_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]