from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Test cases for the Todo model."""

    def setUp(self):
        """Set up test data."""
        self.todo = Todo.objects.create(
            title="Test TODO",
            description="This is a test TODO",
            due_date=date.today() + timedelta(days=7)
        )

    def test_todo_creation(self):
        """Test that a TODO can be created successfully."""
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertEqual(self.todo.description, "This is a test TODO")
        self.assertFalse(self.todo.is_resolved)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_todo_str_representation(self):
        """Test the string representation of a TODO."""
        self.assertEqual(str(self.todo), "Test TODO")

    def test_todo_is_not_overdue(self):
        """Test that a future TODO is not overdue."""
        self.assertFalse(self.todo.is_overdue)

    def test_todo_is_overdue(self):
        """Test that a past TODO is overdue."""
        overdue_todo = Todo.objects.create(
            title="Overdue TODO",
            due_date=date.today() - timedelta(days=1)
        )
        self.assertTrue(overdue_todo.is_overdue)

    def test_completed_todo_not_overdue(self):
        """Test that a completed TODO is never overdue."""
        overdue_todo = Todo.objects.create(
            title="Completed Overdue TODO",
            due_date=date.today() - timedelta(days=1),
            is_resolved=True
        )
        self.assertFalse(overdue_todo.is_overdue)

    def test_todo_without_due_date_not_overdue(self):
        """Test that a TODO without due date is not overdue."""
        no_date_todo = Todo.objects.create(title="No Due Date TODO")
        self.assertFalse(no_date_todo.is_overdue)

    def test_todo_ordering(self):
        """Test that TODOs are ordered by creation date (newest first)."""
        todo1 = Todo.objects.create(title="First")
        todo2 = Todo.objects.create(title="Second")
        todos = Todo.objects.all()
        self.assertEqual(todos[0], todo2)
        self.assertEqual(todos[1], todo1)


class TodoListViewTest(TestCase):
    """Test cases for the TodoListView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.url = reverse('todo-list')

        # Create test TODOs
        Todo.objects.create(title="Active TODO 1", is_resolved=False)
        Todo.objects.create(title="Active TODO 2", is_resolved=False)
        Todo.objects.create(title="Completed TODO", is_resolved=True)

    def test_list_view_status_code(self):
        """Test that the list view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """Test that the correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/home.html')

    def test_list_view_shows_all_todos(self):
        """Test that all TODOs are displayed by default."""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['todos']), 3)

    def test_list_view_filter_active(self):
        """Test filtering active TODOs."""
        response = self.client.get(self.url + '?status=active')
        self.assertEqual(len(response.context['todos']), 2)
        for todo in response.context['todos']:
            self.assertFalse(todo.is_resolved)

    def test_list_view_filter_completed(self):
        """Test filtering completed TODOs."""
        response = self.client.get(self.url + '?status=completed')
        self.assertEqual(len(response.context['todos']), 1)
        for todo in response.context['todos']:
            self.assertTrue(todo.is_resolved)

    def test_list_view_context_data(self):
        """Test that context contains correct counts."""
        response = self.client.get(self.url)
        self.assertEqual(response.context['total_count'], 3)
        self.assertEqual(response.context['active_count'], 2)
        self.assertEqual(response.context['completed_count'], 1)


class TodoCreateViewTest(TestCase):
    """Test cases for the TodoCreateView."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.url = reverse('todo-create')

    def test_create_view_status_code(self):
        """Test that the create view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_template(self):
        """Test that the correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_form.html')

    def test_create_todo_valid_data(self):
        """Test creating a TODO with valid data."""
        data = {
            'title': 'New TODO',
            'description': 'New description',
            'due_date': date.today() + timedelta(days=5)
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'New TODO')
        self.assertEqual(todo.description, 'New description')

    def test_create_todo_without_optional_fields(self):
        """Test creating a TODO without optional fields."""
        data = {'title': 'Minimal TODO'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 1)
        todo = Todo.objects.first()
        self.assertEqual(todo.title, 'Minimal TODO')
        self.assertEqual(todo.description, '')
        self.assertIsNone(todo.due_date)

    def test_create_todo_missing_required_field(self):
        """Test that creating a TODO without title fails."""
        data = {'description': 'No title'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)  # Form redisplayed with errors
        self.assertEqual(Todo.objects.count(), 0)


class TodoUpdateViewTest(TestCase):
    """Test cases for the TodoUpdateView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Original Title",
            description="Original description"
        )
        self.url = reverse('todo-update', args=[self.todo.pk])

    def test_update_view_status_code(self):
        """Test that the update view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_view_template(self):
        """Test that the correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_form.html')

    def test_update_todo_valid_data(self):
        """Test updating a TODO with valid data."""
        data = {
            'title': 'Updated Title',
            'description': 'Updated description',
            'is_resolved': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated description')
        self.assertTrue(self.todo.is_resolved)

    def test_update_nonexistent_todo(self):
        """Test updating a TODO that doesn't exist."""
        url = reverse('todo-update', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    """Test cases for the TodoDeleteView."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.todo = Todo.objects.create(title="To Be Deleted")
        self.url = reverse('todo-delete', args=[self.todo.pk])

    def test_delete_view_status_code(self):
        """Test that the delete view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_template(self):
        """Test that the correct template is used."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')

    def test_delete_todo(self):
        """Test deleting a TODO."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 0)

    def test_delete_nonexistent_todo(self):
        """Test deleting a TODO that doesn't exist."""
        url = reverse('todo-delete', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoToggleResolvedTest(TestCase):
    """Test cases for the toggle_resolved view."""

    def setUp(self):
        """Set up test client and test data."""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Toggle Test",
            is_resolved=False
        )
        self.url = reverse('todo-toggle', args=[self.todo.pk])

    def test_toggle_resolved_to_true(self):
        """Test toggling a TODO from unresolved to resolved."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)

    def test_toggle_resolved_to_false(self):
        """Test toggling a TODO from resolved to unresolved."""
        self.todo.is_resolved = True
        self.todo.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_resolved)

    def test_toggle_nonexistent_todo(self):
        """Test toggling a TODO that doesn't exist."""
        url = reverse('todo-toggle', args=[99999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class URLTest(TestCase):
    """Test cases for URL resolution."""

    def test_todo_list_url_resolves(self):
        """Test that the todo-list URL resolves correctly."""
        url = reverse('todo-list')
        self.assertEqual(url, '/')

    def test_todo_create_url_resolves(self):
        """Test that the todo-create URL resolves correctly."""
        url = reverse('todo-create')
        self.assertEqual(url, '/create/')

    def test_todo_update_url_resolves(self):
        """Test that the todo-update URL resolves correctly."""
        url = reverse('todo-update', args=[1])
        self.assertEqual(url, '/1/edit/')

    def test_todo_delete_url_resolves(self):
        """Test that the todo-delete URL resolves correctly."""
        url = reverse('todo-delete', args=[1])
        self.assertEqual(url, '/1/delete/')

    def test_todo_toggle_url_resolves(self):
        """Test that the todo-toggle URL resolves correctly."""
        url = reverse('todo-toggle', args=[1])
        self.assertEqual(url, '/1/toggle/')
