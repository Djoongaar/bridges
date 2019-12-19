import os

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.urls import reverse
from django.utils.text import slugify
from guardian.shortcuts import assign_perm, remove_perm
# from imagekit.models import ProcessedImageField
# from pilkit.processors import ResizeToFill
from transliterate import translit
from authapp.models import Company, Users
from productsapp.models import TechnicalSolutions


def image_upload_to(instance, filename):
    return 'projects_images/project_{0}/{1}'.format(instance.project.pk, filename)


class Project(models.Model):
    """ Модель проекта строительства со статусом """
    DEVELOPMENT = 'разработка'
    EXPERTISE = 'экспертиза'
    TENDER = 'аукцион'
    EXECUTING = 'строительство'
    FINISHING = 'сдача'
    PAYMENT = 'выплата'
    DONE = 'завершен'

    STATUS_CHOICES = (
        (DEVELOPMENT, 'разработка'),
        (EXPERTISE, 'экспертиза'),
        (TENDER, 'аукцион'),
        (EXECUTING, 'строительство'),
        (FINISHING, 'сдача'),
        (PAYMENT, 'выплата'),
        (DONE, 'завершен'),
    )
    name = models.CharField(verbose_name='Название проекта', max_length=256, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=128, blank=True)
    description = models.TextField(verbose_name='описание', blank=True)
    # image = ProcessedImageField(verbose_name='Аватар', upload_to='projects_images/avatars',
    #                             processors=[ResizeToFill(530, 530)], default='users/avatar/no_avatar.png', blank=True)
    image = models.ImageField(verbose_name='Аватар', upload_to='projects_images/avatars', default='users/avatar/no_avatar.png', blank=True)
    status = models.CharField(verbose_name='Статус', max_length=24, choices=STATUS_CHOICES)
    creation_date = models.DateTimeField(verbose_name='создан', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    city = models.CharField(verbose_name='город', max_length=512, blank=True, null=True)
    address = models.CharField(verbose_name='адрес', max_length=512, blank=True, null=True)
    coordinate = models.CharField(verbose_name='координаты', max_length=34, null=True, blank=True)
    map_mark = models.SlugField(verbose_name='id метки на карте', max_length=128, blank=True)
    is_active = models.BooleanField(verbose_name='активен', default=False)

    def get_absolute_url(self):
        return reverse('projects:project', args=[str(self.id)])

    def get_absolute_discuss_url(self):
        return reverse('projects:project_discuss_items', args=[str(self.id)])

    def __str__(self):
        return f"{self.name} ({self.city})"

    def get_pictures(self):
        return self.images.select_related()

    def get_products(self):
        return self.solutions.select_related()

    def get_companies(self):
        return self.companies.select_related()

    def get_managers(self):
        return self.managers.select_related()

    def get_finished_projects(self):
        pass

    def get_comments(self):
        return self.comments.select_related()

    class Meta:
        ordering = ('-updated',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        default_permissions = ('add', 'change', 'delete')


def pre_save_map_mark(sender, instance, *args, **kwargs):
    if not instance.map_mark:
        map_mark = slugify(translit(instance.name, reversed=True)).replace('-', '_')
        instance.map_mark = map_mark


pre_save.connect(pre_save_map_mark, sender=Project)


class ProjectDiscussItem(models.Model):
    project = models.ForeignKey(Project, verbose_name='проект', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, verbose_name='участник обсуждения', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='добавить сообщение')
    creation_date = models.DateTimeField(verbose_name='создан', auto_now_add=True, auto_now=False)

    def __str__(self):
        return 'комментарий'


class ProjectImage(models.Model):
    """ Галерея фотографий для проекта строительства """
    project = models.ForeignKey(Project, blank=True, null=True, default=None, on_delete=models.CASCADE,
                                related_name="images")
    alt_desc = models.CharField(verbose_name='alt фотографии', max_length=128, blank=True)
    # image = ProcessedImageField(verbose_name='фотографии проекта', upload_to=image_upload_to,
    #                             processors=[ResizeToFill(770, 513)], blank=True)
    image = models.ImageField(verbose_name='фотографии проекта', upload_to=image_upload_to, blank=True)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Фотография проекта'
        verbose_name_plural = 'Фотографии проектов'


class ProjectHasTechnicalSolutions(models.Model):
    """ Модель связи технических решений применяемых на объекте с указанием их объема  """
    name = models.CharField(verbose_name='название конструкции или участка', max_length=256, blank=True, null=True)
    project = models.ForeignKey(Project, verbose_name='Строительный проект', related_name="solutions",
                                on_delete=models.CASCADE)
    techsol = models.ForeignKey(TechnicalSolutions, verbose_name='Техническое решение', related_name='projects',
                                on_delete=models.CASCADE)
    value = models.DecimalField(verbose_name='Объем работ', max_digits=18, decimal_places=2)
    is_active = models.BooleanField(verbose_name='Показывать', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Тех решение проекта'
        verbose_name_plural = 'Тех решения проекта'

    def __str__(self):
        return self.techsol.name


# СВЯЗАНО
class ProjectCompany(models.Model):
    """ Модель связи компаний на объекте """
    DESIGNER = 'проектировщик'
    CONTRACTOR = 'подрядчик'
    CUSTOMER = 'заказчик'
    INSPECTOR = 'инспектор'
    SUPERVISION = 'технический заказчик'
    DESIGNER_SUPERVISION = 'авторский надзор'
    AGENT = 'агент'
    PARTNER = 'партнер'
    STATUS_CHOICES = (
        (DESIGNER, 'проектировщик'),
        (CONTRACTOR, 'подрядчик'),
        (CUSTOMER, 'заказчик'),
        (INSPECTOR, 'инспектор'),
        (SUPERVISION, 'технический заказчик'),
        (DESIGNER_SUPERVISION, 'авторский надзор'),
        (AGENT, 'агент'),
        (PARTNER, 'партнер'),
    )
    project = models.ForeignKey(Project, default=None, on_delete=models.CASCADE,
                                related_name="companies")
    role = models.CharField(verbose_name='роль в проекте', max_length=24, choices=STATUS_CHOICES)
    company = models.ForeignKey(Company, verbose_name='Выберите компанию', default=None,
                                on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Компания - участник проекта'
        verbose_name_plural = 'Компания - участник проекта'

    def __str__(self):
        return self.company.name


# СВЯЗАНО
class ProjectManagers(models.Model):
    """ Модель связи людей на объекте """
    DESIGNER = 'проектировщик'
    CONTRACTOR = 'подрядчик'
    CUSTOMER = 'заказчик'
    INSPECTOR = 'инспектор'
    SUPERVISION = 'технический надзор'
    DESIGNER_SUPERVISION = 'авторский надзор'
    AGENT = 'агент'
    PARTNER = 'партнер'
    MANAGER = 'владелец'
    COMMERSANT = 'коммерсант'
    ASSISTANT = 'ассистент'

    STATUS_CHOICES = (
        (DESIGNER, 'проектировщик'),
        (CONTRACTOR, 'подрядчик'),
        (CUSTOMER, 'заказчик'),
        (INSPECTOR, 'инспектор'),
        (SUPERVISION, 'технический надзор'),
        (DESIGNER_SUPERVISION, 'авторский надзор'),
        (AGENT, 'агент'),
        (PARTNER, 'партнер'),
        (MANAGER, 'владелец'),
        (COMMERSANT, 'коммерсант'),
        (ASSISTANT, 'ассистент'),
    )
    project = models.ForeignKey(Project, verbose_name='проект', on_delete=models.CASCADE, related_name="managers", default=0)
    role = models.CharField(verbose_name='роль в проекте', max_length=24, choices=STATUS_CHOICES)
    manager = models.ForeignKey(Users, verbose_name='Участники', on_delete=models.CASCADE, default=None)
    description = models.TextField(verbose_name='комментарий', blank=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проекта'

    def __str__(self):
        return f"{self.manager.last_name} {self.manager.first_name}"


def project_managers_post_save(sender, instance, created, **kwargs):
    """
    Дает права на изменение профиля проекта после появление менеджера в связанной модели.
    """
    manager = instance.manager
    project = instance.project
    if manager.is_active:
        assign_perm('projectsapp.change_project', manager, project)


post_save.connect(project_managers_post_save, sender=ProjectManagers)


def project_managers_post_delete(sender, instance, **kwargs):
    """
    Дает права на изменение профиля проекта после появление менеджера в связанной модели.
    """
    manager = instance.manager
    project = instance.project
    if manager.is_active:
        remove_perm('projectsapp.change_project', manager, project)


post_delete.connect(project_managers_post_delete, sender=ProjectManagers)
