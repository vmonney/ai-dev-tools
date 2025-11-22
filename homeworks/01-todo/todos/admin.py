from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Admin configuration for Todo model."""
    list_display = ['title', 'due_date', 'is_resolved', 'created_at', 'is_overdue']
    list_filter = ['is_resolved', 'due_date', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Status & Dates', {
            'fields': ('is_resolved', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    actions = ['mark_resolved', 'mark_unresolved']

    def mark_resolved(self, request, queryset):
        """Mark selected TODOs as resolved."""
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f'{updated} TODO(s) marked as resolved.')
    mark_resolved.short_description = 'Mark selected TODOs as resolved'

    def mark_unresolved(self, request, queryset):
        """Mark selected TODOs as unresolved."""
        updated = queryset.update(is_resolved=False)
        self.message_user(request, f'{updated} TODO(s) marked as unresolved.')
    mark_unresolved.short_description = 'Mark selected TODOs as unresolved'
