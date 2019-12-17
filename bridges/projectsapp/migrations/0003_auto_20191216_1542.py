# Generated by Django 2.2 on 2019-12-16 12:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0002_auto_20191216_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdiscussitem',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='создан'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectdiscussitem',
            name='comment',
            field=models.TextField(verbose_name='добавить сообщение'),
        ),
    ]
