# Generated by Django 4.2.2 on 2023-06-11 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]