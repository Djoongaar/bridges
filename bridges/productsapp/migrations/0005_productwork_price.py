# Generated by Django 2.2 on 2019-12-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0004_auto_20191217_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='productwork',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена'),
        ),
    ]
