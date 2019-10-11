# Generated by Django 2.2 on 2019-10-11 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0002_auto_20191011_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='широта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='долгота'),
        ),
    ]