from django.contrib import admin
from .models import Ad, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'views_count', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)