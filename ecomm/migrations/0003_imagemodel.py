# Generated by Django 4.2.2 on 2023-06-11 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0002_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mainimage', models.ImageField(null=True, upload_to='images')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecomm.product')),
            ],
        ),
    ]