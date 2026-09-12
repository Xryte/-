from django.contrib import admin
from .models import PageView


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'ip_address', 'user', 'visited_at')
    list_filter = ('visited_at', 'path')
    search_fields = ('path', 'ip_address', 'user__username')
    readonly_fields = ('path', 'method', 'ip_address', 'user_agent', 'user', 'visited_at')
    date_hierarchy = 'visited_at'