from django.contrib import admin

from .models import Category, Location, Post

admin.site.register(Category)
admin.site.register(Location)


class PostAdmin(admin.ModelAdmin):
    """Настройки административной панели для модели Post."""

    list_display = ('title', 'pub_date', 'is_published', 'category')
    list_filter = ('is_published', 'category', 'pub_date')
    search_fields = ('title', 'text')


admin.site.register(Post, PostAdmin)
