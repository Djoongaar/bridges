# Generated by Django 2.2 on 2019-10-04 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researchapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researchfile',
            old_name='material',
            new_name='research',
        ),
    ]