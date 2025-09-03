from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import LAST_POSTS_COUNT
from .models import Category, Post


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница блога.

    Выводит последние публикации, отсортированные по дате публикации.
    """
    post_list = Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:LAST_POSTS_COUNT]
    context: dict[str, Any] = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Страница отдельной публикации.

    Args:
        id: Идентификатор публикации
    """
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'category',
            'location'
        ),
        id=id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    context: dict[str, Any] = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Страница публикаций в категории.

    Args:
        category_slug: Идентификатор категории
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'author',
        'category',
        'location'
    ).filter(
        is_published=True,
        category=category,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    context: dict[str, Any] = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
