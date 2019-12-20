from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from servicesapp.models import Service
# --------------------------------   МОДЕЛИ ЕДИНИЦ ИЗМЕРЕНИЙ  -------------------------------------
from django.urls import reverse


def image_upload_to(instance, filename):
    return 'products_images/product_{0}/{1}'.format(instance.pk, filename)


def material_image_upload_to(instance, filename):
    return 'products_images/material_{0}/{1}'.format(instance.pk, filename)


def work_image_upload_to(instance, filename):
    return 'products_images/work_{0}/{1}'.format(instance.pk, filename)


class MeasureTypes(models.Model):
    """
    Меры измерений: килограммы, квадратные метры, мегапаскали и др.
    """
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


# -----------------------    МОДЕЛИ ПРОДУКТОВ (ТЕХНИЧЕСКИХ РЕШЕНИЙ)   -------------------------------------


class TechnicalSolutions(models.Model):
    """
    Готовые технические решения (группа материалов собранных в готовый к применению продукт "под ключ"
    и продвигаемый на рынок)
    """
    name = models.CharField(verbose_name='название материала', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=128, unique=True)
    measure = models.ForeignKey(MeasureTypes, verbose_name='Единица измерения', on_delete=models.CASCADE, default=1)
    image = ProcessedImageField(verbose_name='картинка продукта', upload_to=image_upload_to,
                                processors=[ResizeToFill(370, 220)],
                                default='products_images/default-product-image.png', blank=True)
    # image = models.ImageField(verbose_name='картинка продукта', upload_to=image_upload_to,
    #                           default='products_images/default-product-image.png', blank=True)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=500, blank=True)
    short_desc = models.TextField(verbose_name='краткое описание материала', blank=True, null=True)
    description = models.TextField(verbose_name='описание материала', blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    quantity = models. IntegerField(verbose_name='объем работ', default=1)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(verbose_name='активен', default=False)

    def get_absolute_url(self):
        return reverse('products:product', args=[str(self.slug)])

    def get_items(self):
        """Выводит все экземпляры класса"""
        return self.objects.all().order_by('pk')

    def get_active_items(self):
        """Выводит активные экземпляры класса"""
        return self.objects.filter(is_active=True)

    def __str__(self):
        return f"{self.name}"

    def get_projects(self):
        """Выводит уникальные связанные экземпляры класса Project"""
        return self.projects.select_related().distinct('project_id')

    def get_active_projects(self):
        """Выводит уникальные связанные экземпляры класса Project"""
        return self.projects.select_related().distinct('project_id').filter(project__status='завершен')

    def get_works(self):
        return self.works.select_related().order_by('pk')

    def get_materials(self):
        return self.materials.select_related().order_by('pk')

    def get_docs(self):
        return self.docs.select_related()

    class Meta:
        verbose_name = 'Техническое решение'
        verbose_name_plural = 'Технические решения'


class TechnicalSolutionsImage(models.Model):
    """
    Дополнительные картинки к готовому решению
    """
    material = models.ForeignKey(TechnicalSolutions, blank=True, null=True, default=None, on_delete=models.CASCADE)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    image = ProcessedImageField(verbose_name='картинка продукта', upload_to=image_upload_to,
                                processors=[ResizeToFill(370, 220)],
                                default='products_images/default-product-image.png', blank=True)
    # image = models.ImageField(verbose_name='картинка продукта', upload_to=image_upload_to,
    #                           default='products_images/default-product-image.png', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.alt_desc

    class Meta:
        verbose_name = 'Фотография технического решения'
        verbose_name_plural = 'Фотографии технических решений'


# -----------------------    МОДЕЛИ МАТЕРИАЛОВ   -------------------------------------


class MaterialCategory(models.Model):
    """
    Категории материалов: типа грунтовки, мастики, краски, инструмент и др.
    """
    name = models.CharField(verbose_name='категория материала', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория материала'
        verbose_name_plural = 'Категории материалов'


class Material(models.Model):
    """
    Конкретные материалы (торговые марки): Рабберфлекс-55, Гипердесмо, Матакрил и др.
    """
    name = models.CharField(verbose_name='название материала', max_length=128, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=500, unique=True)
    category = models.ForeignKey(MaterialCategory, verbose_name='категория материала', on_delete=models.CASCADE)
    measure = models.ForeignKey(MeasureTypes, verbose_name='Единица измерения', on_delete=models.CASCADE)
    image = ProcessedImageField(verbose_name='картинка материала', upload_to=material_image_upload_to,
                                processors=[ResizeToFill(370, 220)],
                                default='products_images/default-product-image.png', blank=True)
    # image = models.ImageField(verbose_name='картинка материала', upload_to=material_image_upload_to,
    #                           default='products_images/default-product-image.png', blank=True)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    short_desc = models.CharField(verbose_name='краткое описание материала', max_length=500, blank=True, null=True)
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
    """
    Дополнительные картинки к материалам
    """
    material = models.ForeignKey(Material, blank=True, null=True, default=None, on_delete=models.CASCADE)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    image = ProcessedImageField(verbose_name='картинка материала', upload_to=material_image_upload_to,
                                processors=[ResizeToFill(370, 220)],
                                default='products_images/default-product-image.png', blank=True)
    # image = models.ImageField(verbose_name='картинка материала', upload_to=material_image_upload_to,
    #                           default='products_images/default-product-image.png', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.alt_desc

    class Meta:
        verbose_name = 'Фотография материалов'
        verbose_name_plural = 'Фотографии материалов'


# --------------------------------------------    МОДЕЛИ РАБОТ   ------------------------------------------------


class WorkCategory(models.Model):
    """
    Категории работ: типа подготовительные работы, основные работы, испытания, проверка качества.
    """
    name = models.CharField(verbose_name='категория работ', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория работ'
        verbose_name_plural = 'Категории работ'


class Work(models.Model):
    """
    Конкретные работы по техническому решению, например: продувка сжатым воздухом, грунтование,
    нанесение мастики и т.д.
    """
    name = models.CharField(verbose_name='название работ', max_length=128, unique=True)
    category = models.ForeignKey(WorkCategory, verbose_name='категория работ', on_delete=models.CASCADE)
    measure = models.ForeignKey(MeasureTypes, verbose_name='Единица измерения', on_delete=models.CASCADE)
    image = ProcessedImageField(verbose_name='картинка материала', upload_to=work_image_upload_to,
                                processors=[ResizeToFill(370, 220)],
                                default='products_images/default-product-image.png', blank=True)
    # image = models.ImageField(verbose_name='картинка материала', upload_to=work_image_upload_to,
    #                           default='products_images/default-product-image.png', blank=True)
    file = models.FileField(upload_to='products_files', blank=True)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    short_desc = models.CharField(verbose_name='краткое описание материала', max_length=500, blank=True, null=True)
    description = models.TextField(verbose_name='описание материала', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'


class WorkImage(models.Model):
    """
    Дополнительные картинки к работам
    """
    work = models.ForeignKey(Work, blank=True, null=True, default=None, on_delete=models.CASCADE)
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    image = ProcessedImageField(verbose_name='картинка материала', upload_to=work_image_upload_to,
                                processors=[ResizeToFill(370, 220)],
                                default='products_images/default-work-image.png', blank=True)
    # image = models.ImageField(verbose_name='картинка материала', upload_to=work_image_upload_to,
    #                           default='products_images/default-work-image.png', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.alt_desc

    class Meta:
        verbose_name = 'Фотография работ'
        verbose_name_plural = 'Фотографии работ'


class ProductWork(models.Model):
    product = models.ForeignKey(TechnicalSolutions, related_name='works', on_delete=models.CASCADE)
    work = models.ForeignKey(Work, verbose_name='Вид работы', on_delete=models.CASCADE)
    material = models.ManyToManyField(Material, verbose_name='Применяемые материалы', blank=True)
    value = models.DecimalField(verbose_name='трудозатраты', max_digits=8, decimal_places=2, default=0)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Перечень работ продукта'
        verbose_name_plural = 'Перечень работ продукта'


class TechnicalSolutionsHasService(models.Model):
    technicalsolutions = models.ForeignKey(TechnicalSolutions, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name='услуга', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service}"


class ProductMaterial(models.Model):
    product = models.ForeignKey(TechnicalSolutions, related_name='materials', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, verbose_name='Основной материал', related_name='+', on_delete=models.CASCADE)
    alt_materials = models.ManyToManyField(Material, verbose_name='альтернативные материалы', blank=True)
    consumption = models.DecimalField(verbose_name='расход материала', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Перечень материалов продукта'
        verbose_name_plural = 'Перечень материалов продукта'
