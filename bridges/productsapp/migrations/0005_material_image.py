# Generated by Django 2.2.4 on 2019-09-29 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0004_auto_20190929_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='image',
            field=models.ImageField(blank=True, upload_to='products_images'),
        ),
    ]