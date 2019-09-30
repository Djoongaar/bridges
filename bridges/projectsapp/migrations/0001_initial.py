# Generated by Django 2.2.4 on 2019-09-29 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='название')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('image', models.ImageField(blank=True, upload_to='projects_images')),
                ('finishDate', models.DateTimeField()),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('executor', models.CharField(blank=True, max_length=512, null=True)),
                ('orderer', models.CharField(blank=True, max_length=512, null=True)),
                ('designer', models.CharField(blank=True, max_length=512, null=True)),
                ('techDes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productsapp.TechnicalSolutions')),
            ],
        ),
    ]
