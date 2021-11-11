from django.contrib import admin

from reviews.models import Category, Genre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)