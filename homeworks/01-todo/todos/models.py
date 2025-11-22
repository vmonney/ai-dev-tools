from django.db import models
from django.utils import timezone
from django.urls import reverse


class Todo(models.Model):
    """Model representing a TODO item."""
    title = models.CharField(max_length=200, help_text="Title of the TODO")
    description = models.TextField(blank=True, help_text="Detailed description of the TODO")
    due_date = models.DateField(null=True, blank=True, help_text="Due date for the TODO")
    is_resolved = models.BooleanField(default=False, help_text="Whether the TODO is completed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'TODO'
        verbose_name_plural = 'TODOs'

    def __str__(self):
        """String representation of the TODO."""
        return self.title

    @property
    def is_overdue(self):
        """Check if the TODO is overdue."""
        if self.due_date and not self.is_resolved:
            return self.due_date < timezone.now().date()
        return False

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this TODO."""
        return reverse('todo-detail', args=[str(self.id)])
