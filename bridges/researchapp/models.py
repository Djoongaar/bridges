from django.db import models
from authapp.models import Company, Users
from productsapp.models import TechnicalSolutions


class SubjectOfStudy(models.Model):
    """
    Предмет исследования, например "водонепроницаемость", "адгезия" и т.д.
    """
    name = models.CharField(verbose_name='предмет исследования', max_length=128, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет исследование'
        verbose_name_plural = 'Предметы исследований'


class FileStorage(models.Model):
    """
    Файлы или документы подгружаемые к модели Research
    """
    alt_desc = models.CharField(verbose_name='название файла', max_length=128, blank=True)
    file = models.FileField(verbose_name='файл', upload_to='research_files', blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.alt_desc

    class Meta:
        verbose_name = 'Хранилище файлов'
        verbose_name_plural = 'Хранилище файлов'


class DocumentCategory(models.Model):
    """
    Категории документов
    """
    name = models.CharField(verbose_name='название категории', max_length=128, unique=True)
    comment = models.TextField(verbose_name='комментарии', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория документа'
        verbose_name_plural = 'Категории документов'


class Document(models.Model):
    """
    Прочие документы не имеющие отношения к научным работам (отзывы, регламенты, отчеты, заключения
    """
    name = models.CharField(verbose_name='название документа', max_length=128, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    type = models.ForeignKey(DocumentCategory, db_index=True, verbose_name='категория документа', blank=True, null=True,
                             default=None, on_delete=models.CASCADE)
    subject = models.ManyToManyField(SubjectOfStudy, verbose_name='предмет исседования', blank=True)
    company = models.ManyToManyField(Company, verbose_name='компания выпустившая документ', blank=True)
    author = models.ManyToManyField(Users, verbose_name='автор документа', blank=True)
    techsol = models.ManyToManyField(TechnicalSolutions, related_name='docs', verbose_name='техническое решение')
    file = models.ManyToManyField(FileStorage, blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ и исследование'
        verbose_name_plural = 'Документы и исследования'
