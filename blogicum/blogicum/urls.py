from django.contrib import admin
from django.urls import include, path

urlpatterns: list = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
]
