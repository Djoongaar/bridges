# Generated by Django 2.2 on 2019-12-11 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newshastechnicalsolutions',
            name='techsol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productsapp.TechnicalSolutions', verbose_name='Техническое решение'),
        ),
    ]
