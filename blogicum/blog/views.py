from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import LAST_POSTS_COUNT
from .models import Category, Post


def get_post_queryset() -> Any:
    """Возвращает базовый QuerySet для публикаций.

    Returns:
        QuerySet: Отфильтрованный QuerySet с публикациями
    """
    return Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница блога.

    Выводит последние публикации, отсортированные по дате публикации.

    Args:
        request: HTTP-запрос

    Returns:
        HttpResponse: HTML-страница со списком публикаций
    """
    post_list = get_post_queryset()[:LAST_POSTS_COUNT]
    context: dict[str, Any] = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Страница отдельной публикации.

    Args:
        request: HTTP-запрос
        id: Идентификатор публикации

    Returns:
        HttpResponse: HTML-страница с детальной информацией о публикации
    """
    post = get_object_or_404(
        get_post_queryset(),
        id=id
    )
    context: dict[str, Any] = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Страница публикаций в категории.

    Args:
        request: HTTP-запрос
        category_slug: Идентификатор категории

    Returns:
        HttpResponse: HTML-страница со списком публикаций в категории
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_post_queryset().filter(category=category)
    context: dict[str, Any] = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
