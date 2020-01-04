# Generated by Django 2.2 on 2020-01-03 09:43

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0003_auto_20191216_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(default='projects_images/avatars/default_bridge.png', upload_to='projects_images/avatars', verbose_name='Аватар'),
        ),
    ]
