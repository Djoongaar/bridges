# Generated by Django 2.2 on 2019-09-29 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactapp', '0002_auto_20190927_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactapplication',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Имя'),
        ),
    ]
