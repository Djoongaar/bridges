# Generated by Django 2.2 on 2019-12-17 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, verbose_name='цена'),
        ),
    ]
