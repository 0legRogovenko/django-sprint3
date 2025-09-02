from django.contrib.auth import get_user_model
from django.db import models
from typing import Optional


User = get_user_model()


class Category(models.Model):
    """Модель категории для публикаций."""

    title: str = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Заголовок'
    )
    description: str = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание'
    )
    slug: str = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )
    is_published: bool = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""
        return self.title


class Location(models.Model):
    """Модель местоположения публикации."""

    name: str = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Название места'
    )
    is_published: bool = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        """Возвращает строковое представление местоположения."""
        return self.name


class Post(models.Model):
    """Модель публикации в блоге."""

    title: str = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Заголовок'
    )
    text: str = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст'
    )
    pub_date: models.DateTimeField = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )
    author: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location: Optional[models.ForeignKey] = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category: Optional[models.ForeignKey] = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория'
    )
    is_published: bool = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        """Возвращает строковое представление публикации."""
        return self.title
