# Generated by Django 2.2 on 2019-12-17 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0005_productwork_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalsolutions',
            name='quantity',
            field=models.IntegerField(default=1, max_length=10, verbose_name='объем работ'),
        ),
    ]
