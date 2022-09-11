from django.contrib import admin

from core import models


class TaskAdmin(admin.TabularInline):
    model = models.Task
    extra = 1


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    search_fields = ['title', 'description']
    list_display = ['title', 'owner', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    list_per_page = 10
    readonly_fields = ['updated_at', 'created_at']
    inlines = [TaskAdmin]
    