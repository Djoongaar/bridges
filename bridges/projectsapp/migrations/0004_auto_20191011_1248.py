# Generated by Django 2.2 on 2019-10-11 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0003_auto_20191011_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='project',
            name='longitude',
        ),
    ]