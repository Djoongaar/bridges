from django.db import models


class MaterialCategory(models.Model):
    name = models.CharField(verbose_name='категория материала', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория материала'
        verbose_name_plural = 'Категории материалов'


class MeasureTypes(models.Model):
    name = models.CharField(verbose_name='единица измерения', max_length=28, unique=True)
    shortcut = models.CharField(verbose_name='ед.изм.', max_length=10, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.shortcut

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


# class Characteristic(models.Model):
#     name = models.CharField(verbose_name='название характеристики', max_length=28, unique=True)
#     measure = models.ForeignKey(MeasureTypes, on_delete=models.CASCADE)
#     description = models.TextField(verbose_name='описание', blank=True)
#
#     def __str__(self):
#         return f"{self.name} {self.measure}"


class Material(models.Model):
    name = models.CharField(verbose_name='название материала', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=128, unique=True)
    category = models.ForeignKey(MaterialCategory,verbose_name='категория материала', on_delete=models.CASCADE)
    measure = models.ForeignKey(MeasureTypes, verbose_name='Единица измерения', on_delete=models.CASCADE)
    # characteristics = models.ManyToManyField(Characteristic)
    image = models.ImageField(upload_to='products_images', blank=True)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    short_desc = models.CharField(verbose_name='краткое описание материала', max_length=500, blank=True)
    description = models.TextField(verbose_name='описание материала', blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'


class MaterialImage(models.Model):
    material = models.ForeignKey(Material, blank=True, null=True, default=None, on_delete=models.CASCADE)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='products_images', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.alt_desc

    class Meta:
        verbose_name = 'Фотография материаллов'
        verbose_name_plural = 'Фотографии материаллов'


class TechnicalSolutions(models.Model):
    material_content = models.ManyToManyField(Material)
    image = models.ImageField(upload_to='products_images', blank=True)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    description = models.TextField(verbose_name='описание материала', blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Техническое решение'
        verbose_name_plural = 'Технические решения'


class TechnicalSolutionsImage(models.Model):
    material = models.ForeignKey(TechnicalSolutions, blank=True, null=True, default=None, on_delete=models.CASCADE)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='products_images', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.alt_desc

    class Meta:
        verbose_name = 'Фотография технического решения'
        verbose_name_plural = 'Фотографии технических решений'
