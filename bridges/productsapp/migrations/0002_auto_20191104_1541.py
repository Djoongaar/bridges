# Generated by Django 2.2 on 2019-11-04 12:41

from django.db import migrations
import imagekit.models.fields
import productsapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='products_images/default-product-image.png', upload_to=productsapp.models.material_image_upload_to, verbose_name='картинка материала'),
        ),
        migrations.AlterField(
            model_name='materialimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='products_images/default-product-image.png', upload_to=productsapp.models.material_image_upload_to, verbose_name='картинка материала'),
        ),
        migrations.AlterField(
            model_name='technicalsolutions',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='products_images/default-product-image.png', upload_to=productsapp.models.image_upload_to, verbose_name='картинка продукта'),
        ),
        migrations.AlterField(
            model_name='technicalsolutionsimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='products_images/default-product-image.png', upload_to=productsapp.models.image_upload_to, verbose_name='картинка продукта'),
        ),
        migrations.AlterField(
            model_name='work',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='products_images/default-product-image.png', upload_to=productsapp.models.work_image_upload_to, verbose_name='картинка материала'),
        ),
        migrations.AlterField(
            model_name='workimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='products_images/default-work-image.png', upload_to=productsapp.models.work_image_upload_to, verbose_name='картинка материала'),
        ),
    ]