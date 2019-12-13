# Generated by Django 2.2 on 2019-12-11 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productsapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='название')),
                ('slug', models.SlugField(max_length=128, unique=True, verbose_name='слаг')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, default='news_avatars/no_news.jpg', upload_to='news_avatars', verbose_name='картинка новости')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='обновлен')),
                ('status', models.CharField(choices=[('FORMING', 'FORMING'), ('REDACTION', 'REDACTION'), ('READY', 'READY')], default='FORMING', max_length=20, verbose_name='статус')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ('-updated',),
            },
        ),
        migrations.CreateModel(
            name='NewsHasTechnicalSolutions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='название конструкции или участка')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='newsapp.News', verbose_name='Новость')),
                ('techsol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='productsapp.TechnicalSolutions', verbose_name='Техническое решение')),
            ],
            options={
                'verbose_name': 'Тех решение проекта',
                'verbose_name_plural': 'Тех решения проекта',
            },
        ),
        migrations.CreateModel(
            name='NewsDiscussItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1500, verbose_name='добавить сообщение')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsapp.News', verbose_name='новость обсуждения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='участник обсуждения')),
            ],
        ),
    ]