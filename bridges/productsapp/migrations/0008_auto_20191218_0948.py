# Generated by Django 2.2 on 2019-12-18 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productsapp', '0007_auto_20191217_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productwork',
            name='consumption',
        ),
        migrations.RemoveField(
            model_name='work',
            name='materials',
        ),
        migrations.RemoveField(
            model_name='work',
            name='price',
        ),
        migrations.CreateModel(
            name='ProductMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumption', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='расход материала')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productsapp.Material', verbose_name='Применяемые материалы')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='productsapp.TechnicalSolutions')),
            ],
            options={
                'verbose_name': 'Перечень материалов продукта',
                'verbose_name_plural': 'Перечень материалов продукта',
            },
        ),
    ]