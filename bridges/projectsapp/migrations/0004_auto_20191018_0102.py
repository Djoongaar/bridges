# Generated by Django 2.2 on 2019-10-17 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0003_auto_20191016_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmanagers',
            name='project',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='managers', to='projectsapp.Project', verbose_name='проект'),
        ),
    ]