# Generated by Django 2.2 on 2019-11-06 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-updated',), 'permissions': (('update_project', 'Update project'),), 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
    ]
