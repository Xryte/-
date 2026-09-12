from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Ad(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='ads/%Y/%m/', blank=True, null=True)
    link = models.URLField('Ссылка', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ads',
        verbose_name='Категория'
    )
    is_active = models.BooleanField('Активно', default=True)
    views_count = models.PositiveIntegerField('Просмотров', default=0)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views(self):
        Ad.objects.filter(pk=self.pk).update(views_count=models.F('views_count') + 1)