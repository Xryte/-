from django.db import models
from django.conf import settings


class PageView(models.Model):
    path = models.CharField('Путь', max_length=500, db_index=True)
    method = models.CharField('Метод', max_length=10, default='GET')
    ip_address = models.GenericIPAddressField('IP', null=True, blank=True)
    user_agent = models.CharField('User-Agent', max_length=500, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    visited_at = models.DateTimeField('Время посещения', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'
        ordering = ['-visited_at']
        indexes = [
            models.Index(fields=['-visited_at']),
            models.Index(fields=['path', '-visited_at']),
        ]

    def __str__(self):
        return f'{self.path} — {self.ip_address} — {self.visited_at}'