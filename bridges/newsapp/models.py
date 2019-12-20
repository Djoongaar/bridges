from django.db import models
from django.http import request
from django.urls import reverse
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from productsapp.models import TechnicalSolutions
from authapp.models import Users


class News(models.Model):
    """ Модель новости"""
    DELETED = 'DELETED'
    FORMING = 'FORMING'
    REDACTION = 'REDACTION'
    READY = 'READY'
    NEWS_STATUS_CHOICES = (
        (DELETED, 'DELETED'),
        (FORMING, 'FORMING'),
        (REDACTION, 'REDACTION'),
        (READY, 'READY'),
    )
    name = models.CharField(verbose_name='название', max_length=256, unique=True)
    slug = models.SlugField(verbose_name='слаг', max_length=128, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    image = ProcessedImageField(verbose_name='картинка новости', upload_to='news_avatars',
                                processors=[ResizeToFill(370, 220)], default='news_avatars/no_news.jpg', blank=True)
    # image = models.ImageField(verbose_name='картинка новости', upload_to='news_avatars',
    #                           default='news_avatars/no_news.jpg', blank=True)
    creation_date = models.DateTimeField(verbose_name='создан', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    author = models.ForeignKey(Users, verbose_name='Автор', on_delete=models.CASCADE, default=1)
    status = models.CharField(verbose_name='статус', max_length=20, choices=NEWS_STATUS_CHOICES, default=FORMING)

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[str(self.pk)])

    class Meta:
        ordering = ('-updated',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def get_products(self):
        return self.solutions.select_related()

    def get_comments(self):
        return self.comments.select_related()

    def get_count_comments(self):
        return len(self.comments.select_related())

    def __str__(self):
        return self.name


class NewsProduct(models.Model):
    """ Модель связи продукта и новости  """
    news = models.ForeignKey(News, verbose_name='Новость', related_name="solutions",
                             on_delete=models.CASCADE)
    techsol = models.ForeignKey(TechnicalSolutions, verbose_name='Техническое решение', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Тех решение проекта'
        verbose_name_plural = 'Тех решения проекта'

    def __str__(self):
        return f"{self.news}: {self.techsol}"


class NewsDiscussItem(models.Model):
    news = models.ForeignKey(News, verbose_name='новость обсуждения', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, verbose_name='участник обсуждения', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='добавить сообщение', max_length=1500)
    creation_date = models.DateTimeField(verbose_name='создан', auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.comment
