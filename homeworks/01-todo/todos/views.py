from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    """Custom form for TODO with date format help."""
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'YYYY-MM-DD'
        }),
        help_text='Format: YYYY-MM-DD (e.g., 2025-12-31) or use the date picker'
    )

    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date']


class TodoUpdateForm(TodoForm):
    """Form for updating TODO with is_resolved field."""
    class Meta:
        model = Todo
        fields = ['title', 'description', 'due_date', 'is_resolved']


class TodoListView(ListView):
    """View to display all TODOs with filtering options."""
    model = Todo
    template_name = 'todos/home.html'
    context_object_name = 'todos'
    paginate_by = 10

    def get_queryset(self):
        """Filter TODOs based on status parameter."""
        queryset = super().get_queryset()
        status = self.request.GET.get('status', 'all')

        if status == 'active':
            queryset = queryset.filter(is_resolved=False)
        elif status == 'completed':
            queryset = queryset.filter(is_resolved=True)

        return queryset

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('status', 'all')
        context['total_count'] = Todo.objects.count()
        context['active_count'] = Todo.objects.filter(is_resolved=False).count()
        context['completed_count'] = Todo.objects.filter(is_resolved=True).count()
        return context


class TodoCreateView(CreateView):
    """View to create a new TODO."""
    model = Todo
    template_name = 'todos/todo_form.html'
    form_class = TodoForm
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        """Add success message when TODO is created."""
        messages.success(self.request, f'TODO "{form.instance.title}" created successfully!')
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    """View to update an existing TODO."""
    model = Todo
    template_name = 'todos/todo_form.html'
    form_class = TodoUpdateForm
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        """Add success message when TODO is updated."""
        messages.success(self.request, f'TODO "{form.instance.title}" updated successfully!')
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    """View to delete a TODO."""
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')

    def delete(self, request, *args, **kwargs):
        """Add success message when TODO is deleted."""
        todo = self.get_object()
        messages.success(request, f'TODO "{todo.title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


def toggle_resolved(request, pk):
    """Toggle the resolved status of a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()

    status = "completed" if todo.is_resolved else "reopened"
    messages.success(request, f'TODO "{todo.title}" marked as {status}!')

    return redirect('todo-list')
