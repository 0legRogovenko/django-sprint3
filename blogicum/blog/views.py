from typing import Any
from django.utils import timezone
from django.http import HttpRequest, HttpResponse


from django.shortcuts import render, get_object_or_404


from .models import Post, Category


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context: dict[str, Any] = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related('category'), 
        id=id, 
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    context: dict[str, Any] = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.filter(
        is_published=True,
        category=category,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    context: dict[str, Any] = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
