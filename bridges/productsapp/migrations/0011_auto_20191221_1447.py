# Generated by Django 2.2 on 2019-12-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0010_auto_20191218_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicalsolutions',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='активен'),
        ),
    ]