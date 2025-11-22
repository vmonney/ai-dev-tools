# Building a Django TODO Application from Scratch

A comprehensive guide for Python developers new to Django. This tutorial will walk you through building a fully-functional TODO application with create, read, update, and delete (CRUD) operations.

---

## Table of Contents

1. [Introduction to Django](#introduction-to-django)
2. [Prerequisites](#prerequisites)
3. [Understanding Django Architecture](#understanding-django-architecture)
4. [Setting Up Your Development Environment](#setting-up-your-development-environment)
5. [Creating Your Django Project](#creating-your-django-project)
6. [Creating a Django App](#creating-a-django-app)
7. [Understanding Models (The Database Layer)](#understanding-models-the-database-layer)
8. [Working with Migrations](#working-with-migrations)
9. [Setting Up the Admin Panel](#setting-up-the-admin-panel)
10. [Creating Views (The Logic Layer)](#creating-views-the-logic-layer)
11. [URL Routing](#url-routing)
12. [Templates (The Presentation Layer)](#templates-the-presentation-layer)
13. [Testing Your Application](#testing-your-application)
14. [Running the Development Server](#running-the-development-server)
15. [Next Steps and Best Practices](#next-steps-and-best-practices)

---

## Introduction to Django

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the **MTV (Model-Template-View)** pattern, which is similar to MVC (Model-View-Controller).

**Key Django Principles:**
- **Don't Repeat Yourself (DRY)**: Write code once and reuse it
- **Batteries Included**: Comes with built-in features like authentication, admin panel, ORM
- **Security First**: Protects against SQL injection, XSS, CSRF, and more
- **Scalable**: Powers sites like Instagram, Pinterest, and Mozilla

---

## Prerequisites

Before starting, you should have:
- Python 3.8 or higher installed
- Basic understanding of Python programming
- Familiarity with command-line interfaces
- A text editor or IDE (VS Code, PyCharm, etc.)

---

## Understanding Django Architecture

Django uses the **MTV (Model-Template-View)** architecture:

```
┌─────────────────────────────────────────────┐
│              User's Browser                 │
└─────────────────────────────────────────────┘
                    ↓ HTTP Request
┌─────────────────────────────────────────────┐
│              URL Dispatcher                 │
│  (urls.py - Routes URLs to views)           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│                 View                        │
│  (views.py - Business logic)                │
│  ↕                                          │
│  Model (models.py - Database interface)     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│               Template                      │
│  (HTML files - Presentation)                │
└─────────────────────────────────────────────┘
                    ↓ HTTP Response
┌─────────────────────────────────────────────┐
│              User's Browser                 │
└─────────────────────────────────────────────┘
```

**Components:**
- **Model**: Defines your data structure (Python classes → Database tables)
- **Template**: HTML files with Django template language for dynamic content
- **View**: Python functions/classes that handle requests and return responses
- **URL Dispatcher**: Maps URLs to views

---

## Setting Up Your Development Environment

### Step 1: Create a Project Directory

```bash
mkdir django-todo-app
cd django-todo-app
```

### Step 2: Set Up a Virtual Environment

A virtual environment isolates your project's dependencies.

**Using `uv` (Recommended - Fast and Modern):**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows
```

**Using Standard Python (Alternative):**
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
# OR
venv\Scripts\activate      # On Windows
```

### Step 3: Install Django

**With `uv`:**
```bash
uv pip install django
```

**With standard pip:**
```bash
pip install django
```

This will install:
- Django (the framework)
- asgiref (ASGI server reference implementation)
- sqlparse (SQL parser for formatting)

**Verify Installation:**
```bash
python -m django --version
```

---

## Creating Your Django Project

A **Django project** is a collection of settings and apps. Think of it as your website's container.

### Create the Project

```bash
django-admin startproject todoproject .
```

**Note the `.` at the end** - this creates the project in the current directory instead of creating a subdirectory.

### Project Structure

```
django-todo-app/
├── manage.py              # Command-line utility for Django commands
└── todoproject/           # Project package
    ├── __init__.py        # Makes this a Python package
    ├── settings.py        # Project settings and configuration
    ├── urls.py            # URL declarations (routing table)
    ├── asgi.py            # ASGI deployment entry point
    └── wsgi.py            # WSGI deployment entry point
```

**Important Files:**
- **manage.py**: Your command-line tool for this project (run server, migrations, tests, etc.)
- **settings.py**: All project settings (database, installed apps, middleware, etc.)
- **urls.py**: URL routing for the entire project

---

## Creating a Django App

A **Django app** is a web application that does something specific (e.g., a blog, a poll system, a TODO list). Projects can contain multiple apps.

### Create the App

```bash
python manage.py startapp todos
```

### App Structure

```
todos/
├── __init__.py            # Makes this a Python package
├── admin.py               # Admin panel configuration
├── apps.py                # App configuration
├── models.py              # Data models (database schema)
├── views.py               # View functions/classes (logic)
├── tests.py               # Test cases
└── migrations/            # Database migration files
    └── __init__.py
```

### Register the App

Open `todoproject/settings.py` and add your app to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "todos",  # Add this line
]
```

**Why?** Django needs to know about your app to include it in migrations, admin panel, and other operations.

---

## Understanding Models (The Database Layer)

Models define your data structure. Each model is a Python class that becomes a database table.

### The Todo Model

Create your model in `todos/models.py`:

```python
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Todo(models.Model):
    """Model representing a TODO item."""

    # Fields (become database columns)
    title = models.CharField(
        max_length=200,
        help_text="Title of the TODO"
    )

    description = models.TextField(
        blank=True,
        help_text="Detailed description of the TODO"
    )

    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="Due date for the TODO"
    )

    is_resolved = models.BooleanField(
        default=False,
        help_text="Whether the TODO is completed"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = 'TODO'
        verbose_name_plural = 'TODOs'

    def __str__(self):
        """String representation shown in admin and shell."""
        return self.title

    @property
    def is_overdue(self):
        """Check if the TODO is overdue."""
        if self.due_date and not self.is_resolved:
            return self.due_date < timezone.now().date()
        return False

    def get_absolute_url(self):
        """Returns the URL to access a detail record."""
        return reverse('todo-detail', args=[str(self.id)])
```

### Understanding Field Types

| Field Type | Database Type | Use Case |
|------------|---------------|----------|
| `CharField` | VARCHAR | Short text (max_length required) |
| `TextField` | TEXT | Long text (no length limit) |
| `DateField` | DATE | Date only (year, month, day) |
| `DateTimeField` | TIMESTAMP | Date and time |
| `BooleanField` | BOOLEAN | True/False values |
| `IntegerField` | INTEGER | Whole numbers |
| `EmailField` | VARCHAR | Email addresses (with validation) |

### Field Options

- **`blank=True`**: Field can be empty in forms
- **`null=True`**: Database allows NULL values
- **`default=value`**: Default value if not specified
- **`auto_now_add=True`**: Set to current datetime when created
- **`auto_now=True`**: Update to current datetime on every save
- **`max_length=n`**: Maximum length (required for CharField)

### Meta Class

The `Meta` class contains metadata:
- **`ordering`**: Default sort order for queries
- **`verbose_name`**: Human-readable singular name
- **`verbose_name_plural`**: Human-readable plural name

---

## Working with Migrations

Migrations are Django's way of propagating changes you make to your models into your database schema.

### The Migration Process

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  Change      │      │  Create      │      │  Apply to    │
│  models.py   │  →   │  Migration   │  →   │  Database    │
│              │      │  Files       │      │              │
└──────────────┘      └──────────────┘      └──────────────┘
```

### Step 1: Create Migrations

```bash
python manage.py makemigrations
```

**Output:**
```
Migrations for 'todos':
  todos/migrations/0001_initial.py
    + Create model Todo
```

This creates a migration file in `todos/migrations/0001_initial.py` that contains instructions to create the database table.

### Step 2: View SQL (Optional)

To see the SQL that will be executed:
```bash
python manage.py sqlmigrate todos 0001
```

### Step 3: Apply Migrations

```bash
python manage.py migrate
```

**Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, todos
Running migrations:
  Applying todos.0001_initial... OK
```

This creates the actual database tables.

### When to Run Migrations

Run migrations whenever you:
- Create a new model
- Add/remove/modify model fields
- Change Meta options that affect the database

### Common Migration Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Revert to a specific migration
python manage.py migrate todos 0001
```

---

## Setting Up the Admin Panel

Django's admin panel is a powerful, automatic CRUD interface for your models.

### Step 1: Register Your Model

Edit `todos/admin.py`:

```python
from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """Admin configuration for Todo model."""

    # Columns to display in list view
    list_display = [
        'title',
        'due_date',
        'is_resolved',
        'created_at',
        'is_overdue'
    ]

    # Filters in sidebar
    list_filter = [
        'is_resolved',
        'due_date',
        'created_at'
    ]

    # Search functionality
    search_fields = [
        'title',
        'description'
    ]

    # Date hierarchy navigation
    date_hierarchy = 'created_at'

    # Default ordering
    ordering = ['-created_at']

    # Organize fields into sections
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Status & Dates', {
            'fields': ('is_resolved', 'due_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )

    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']

    # Bulk actions
    actions = ['mark_resolved', 'mark_unresolved']

    def mark_resolved(self, request, queryset):
        """Mark selected TODOs as resolved."""
        updated = queryset.update(is_resolved=True)
        self.message_user(
            request,
            f'{updated} TODO(s) marked as resolved.'
        )
    mark_resolved.short_description = 'Mark selected TODOs as resolved'

    def mark_unresolved(self, request, queryset):
        """Mark selected TODOs as unresolved."""
        updated = queryset.update(is_resolved=False)
        self.message_user(
            request,
            f'{updated} TODO(s) marked as unresolved.'
        )
    mark_unresolved.short_description = 'Mark selected TODOs as unresolved'
```

### Step 2: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
```

### Step 3: Access the Admin Panel

Start the server (we'll cover this later) and visit:
```
http://127.0.0.1:8000/admin/
```

---

## Creating Views (The Logic Layer)

Views handle the business logic and connect models with templates.

### Types of Views

1. **Function-Based Views (FBVs)**: Simple functions
2. **Class-Based Views (CBVs)**: Reusable classes with common patterns

We'll use CBVs for CRUD operations because they reduce code duplication.

### Create Views in `todos/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Todo


class TodoListView(ListView):
    """Display all TODOs with filtering."""
    model = Todo
    template_name = 'todos/home.html'
    context_object_name = 'todos'
    paginate_by = 10  # Show 10 items per page

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
        """Add extra context for template."""
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('status', 'all')
        context['total_count'] = Todo.objects.count()
        context['active_count'] = Todo.objects.filter(
            is_resolved=False
        ).count()
        context['completed_count'] = Todo.objects.filter(
            is_resolved=True
        ).count()
        return context


class TodoCreateView(CreateView):
    """Create a new TODO."""
    model = Todo
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'due_date']
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        """Called when valid form data has been POSTed."""
        messages.success(
            self.request,
            f'TODO "{form.instance.title}" created successfully!'
        )
        return super().form_valid(form)


class TodoUpdateView(UpdateView):
    """Update an existing TODO."""
    model = Todo
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'due_date', 'is_resolved']
    success_url = reverse_lazy('todo-list')

    def form_valid(self, form):
        """Called when valid form data has been POSTed."""
        messages.success(
            self.request,
            f'TODO "{form.instance.title}" updated successfully!'
        )
        return super().form_valid(form)


class TodoDeleteView(DeleteView):
    """Delete a TODO."""
    model = Todo
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')

    def delete(self, request, *args, **kwargs):
        """Called when DELETE is confirmed."""
        todo = self.get_object()
        messages.success(
            request,
            f'TODO "{todo.title}" deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)


def toggle_resolved(request, pk):
    """Toggle the resolved status of a TODO."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_resolved = not todo.is_resolved
    todo.save()

    status = "completed" if todo.is_resolved else "reopened"
    messages.success(
        request,
        f'TODO "{todo.title}" marked as {status}!'
    )

    return redirect('todo-list')
```

### Understanding Class-Based Views

| View Class | Purpose | Methods to Override |
|------------|---------|---------------------|
| `ListView` | Display list of objects | `get_queryset()`, `get_context_data()` |
| `CreateView` | Create new object | `form_valid()`, `get_success_url()` |
| `UpdateView` | Update existing object | `form_valid()`, `get_success_url()` |
| `DeleteView` | Delete object | `delete()`, `get_success_url()` |

---

## URL Routing

URLs map web addresses to views.

### Step 1: Create App URLs

Create `todos/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TodoListView.as_view(), name='todo-list'),
    path('create/', views.TodoCreateView.as_view(), name='todo-create'),
    path('<int:pk>/edit/', views.TodoUpdateView.as_view(), name='todo-update'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='todo-delete'),
    path('<int:pk>/toggle/', views.toggle_resolved, name='todo-toggle'),
]
```

**URL Pattern Syntax:**
- `''` - Empty string matches root URL
- `'create/'` - Matches `/create/`
- `'<int:pk>'` - Captures integer as `pk` variable
- `name='...'` - Name for reversing URLs in templates

### Step 2: Include App URLs in Project

Edit `todoproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todos.urls")),  # Include todos URLs
]
```

### URL Structure

```
http://127.0.0.1:8000/          → TodoListView
http://127.0.0.1:8000/create/   → TodoCreateView
http://127.0.0.1:8000/1/edit/   → TodoUpdateView (pk=1)
http://127.0.0.1:8000/1/delete/ → TodoDeleteView (pk=1)
http://127.0.0.1:8000/1/toggle/ → toggle_resolved (pk=1)
http://127.0.0.1:8000/admin/    → Admin panel
```

---

## Templates (The Presentation Layer)

Templates are HTML files with Django's template language for dynamic content.

### Step 1: Configure Template Directory

Edit `todoproject/settings.py`:

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "todos" / "templates"],  # Add this
        "APP_DIRS": True,
        # ... rest of configuration
    },
]
```

### Step 2: Create Directory Structure

```bash
mkdir -p todos/templates/todos
```

### Step 3: Create Base Template

`todos/templates/todos/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TODO App{% endblock %}</title>
    <style>
        /* Add your CSS here */
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        /* ... more styles ... */
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <h1>TODO Application</h1>
        <nav>
            <a href="{% url 'todo-list' %}">Home</a>
            <a href="{% url 'todo-create' %}">New TODO</a>
            <a href="/admin/">Admin</a>
        </nav>
    </header>

    <main>
        {% if messages %}
        <div class="messages">
            {% for message in messages %}
            <div class="message {{ message.tags }}">
                {{ message }}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        {% block content %}
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2025 TODO App</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Step 4: Create Home Template

`todos/templates/todos/home.html`:

```html
{% extends 'todos/base.html' %}

{% block title %}TODO List - {{ block.super }}{% endblock %}

{% block content %}
<h2>My TODOs</h2>

<!-- Statistics -->
<div class="stats">
    <div>Total: {{ total_count }}</div>
    <div>Active: {{ active_count }}</div>
    <div>Completed: {{ completed_count }}</div>
</div>

<!-- Filters -->
<div class="filters">
    <a href="?status=all">All</a>
    <a href="?status=active">Active</a>
    <a href="?status=completed">Completed</a>
</div>

<!-- TODO List -->
{% if todos %}
    {% for todo in todos %}
    <div class="todo-item {% if todo.is_resolved %}resolved{% endif %}">
        <h3>{{ todo.title }}</h3>

        {% if todo.description %}
        <p>{{ todo.description }}</p>
        {% endif %}

        <div class="meta">
            <span>Created: {{ todo.created_at|date:"M d, Y" }}</span>

            {% if todo.due_date %}
            <span>Due: {{ todo.due_date|date:"M d, Y" }}</span>
            {% if todo.is_overdue %}
                <span class="badge overdue">OVERDUE</span>
            {% endif %}
            {% endif %}
        </div>

        <div class="actions">
            <a href="{% url 'todo-toggle' todo.pk %}">
                {% if todo.is_resolved %}Reopen{% else %}Complete{% endif %}
            </a>
            <a href="{% url 'todo-update' todo.pk %}">Edit</a>
            <a href="{% url 'todo-delete' todo.pk %}">Delete</a>
        </div>
    </div>
    {% endfor %}
{% else %}
    <p>No TODOs found. <a href="{% url 'todo-create' %}">Create one!</a></p>
{% endif %}
{% endblock %}
```

### Step 5: Create Form Template

`todos/templates/todos/todo_form.html`:

```html
{% extends 'todos/base.html' %}

{% block title %}
{% if object %}Edit TODO{% else %}Create TODO{% endif %} - {{ block.super }}
{% endblock %}

{% block content %}
<h2>{% if object %}Edit TODO{% else %}Create New TODO{% endif %}</h2>

<form method="post">
    {% csrf_token %}

    <div class="form-group">
        <label for="{{ form.title.id_for_label }}">Title *</label>
        {{ form.title }}
        {% if form.title.errors %}
            {{ form.title.errors }}
        {% endif %}
    </div>

    <div class="form-group">
        <label for="{{ form.description.id_for_label }}">Description</label>
        {{ form.description }}
    </div>

    <div class="form-group">
        <label for="{{ form.due_date.id_for_label }}">Due Date</label>
        {{ form.due_date }}
    </div>

    {% if object %}
    <div class="form-group">
        {{ form.is_resolved }}
        <label for="{{ form.is_resolved.id_for_label }}">Completed</label>
    </div>
    {% endif %}

    <div class="form-actions">
        <a href="{% url 'todo-list' %}">Cancel</a>
        <button type="submit">
            {% if object %}Update{% else %}Create{% endif %}
        </button>
    </div>
</form>
{% endblock %}
```

### Step 6: Create Delete Confirmation Template

`todos/templates/todos/todo_confirm_delete.html`:

```html
{% extends 'todos/base.html' %}

{% block title %}Delete TODO - {{ block.super }}{% endblock %}

{% block content %}
<h2>Confirm Deletion</h2>

<div class="warning">
    <p>Are you sure you want to delete "<strong>{{ object.title }}</strong>"?</p>
    <p>This action cannot be undone.</p>
</div>

<form method="post">
    {% csrf_token %}
    <a href="{% url 'todo-list' %}">Cancel</a>
    <button type="submit" class="btn-danger">Yes, Delete</button>
</form>
{% endblock %}
```

### Template Language Basics

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ variable }}` | Output variable | `{{ todo.title }}` |
| `{% tag %}` | Template tag | `{% if todos %}` |
| `{% block %}` | Define block | `{% block content %}` |
| `{% extends %}` | Inherit template | `{% extends 'base.html' %}` |
| `{% url %}` | Reverse URL | `{% url 'todo-list' %}` |
| `{% csrf_token %}` | CSRF protection | Required in forms |
| `{{ var\|filter }}` | Apply filter | `{{ date\|date:"Y-m-d" }}` |

---

## Testing Your Application

Testing ensures your code works correctly and prevents regressions.

### Create Tests in `todos/tests.py`

```python
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import Todo


class TodoModelTest(TestCase):
    """Test the Todo model."""

    def setUp(self):
        """Create test data."""
        self.todo = Todo.objects.create(
            title="Test TODO",
            due_date=date.today() + timedelta(days=7)
        )

    def test_todo_creation(self):
        """Test creating a TODO."""
        self.assertEqual(self.todo.title, "Test TODO")
        self.assertFalse(self.todo.is_resolved)

    def test_todo_str(self):
        """Test string representation."""
        self.assertEqual(str(self.todo), "Test TODO")

    def test_is_overdue(self):
        """Test overdue detection."""
        overdue_todo = Todo.objects.create(
            title="Overdue",
            due_date=date.today() - timedelta(days=1)
        )
        self.assertTrue(overdue_todo.is_overdue)


class TodoViewTest(TestCase):
    """Test the views."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()
        self.todo = Todo.objects.create(title="Test")

    def test_list_view(self):
        """Test list view loads."""
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

    def test_create_view(self):
        """Test creating a TODO."""
        data = {'title': 'New TODO'}
        response = self.client.post(
            reverse('todo-create'),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Todo.objects.count(), 2)
```

### Run Tests

```bash
python manage.py test
```

**Output:**
```
Found X test(s).
Creating test database...
....................
----------------------------------------------------------------------
Ran X tests in 0.XXXs

OK
```

### Test Types

- **Model Tests**: Test model methods, properties, and validation
- **View Tests**: Test HTTP responses, redirects, and contexts
- **Form Tests**: Test form validation and processing
- **Integration Tests**: Test complete workflows

---

## Running the Development Server

### Start the Server

```bash
python manage.py runserver
```

**Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 5.2.8, using settings 'todoproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Access Your Application

- **Main app**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

### Custom Port

```bash
python manage.py runserver 8080
```

### Allow External Access

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Next Steps and Best Practices

### Production Checklist

1. **Security**:
   - Change `SECRET_KEY` and keep it secret
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use HTTPS

2. **Database**:
   - Switch from SQLite to PostgreSQL/MySQL
   - Set up database backups

3. **Static Files**:
   - Configure `STATIC_ROOT`
   - Run `python manage.py collectstatic`

4. **Dependencies**:
   - Create `requirements.txt`:
     ```bash
     pip freeze > requirements.txt
     ```

5. **Environment Variables**:
   - Use python-decouple or django-environ
   - Store secrets in `.env` file

### Deployment Options

- **Heroku**: Easy deployment with free tier
- **PythonAnywhere**: Python-focused hosting
- **DigitalOcean**: Full control with droplets
- **AWS/Google Cloud**: Scalable enterprise solutions

### Further Learning

1. **Django Features**:
   - User authentication and permissions
   - Django REST Framework for APIs
   - Django forms and form validation
   - Middleware and signals
   - Caching and performance optimization

2. **Advanced Topics**:
   - Custom user models
   - Many-to-many relationships
   - File uploads and media handling
   - Celery for background tasks
   - WebSockets with Django Channels

3. **Tools**:
   - Django Debug Toolbar
   - Django Extensions
   - Pytest for Django
   - Coverage.py for test coverage

### Resources

- **Official Django Documentation**: https://docs.djangoproject.com/
- **Django Girls Tutorial**: https://tutorial.djangogirls.org/
- **Django for Beginners**: Book by William S. Vincent
- **Two Scoops of Django**: Best practices book

---

## Summary

You've learned how to:

1. ✅ Set up a Django development environment
2. ✅ Create a Django project and app
3. ✅ Define models and work with migrations
4. ✅ Set up the admin panel
5. ✅ Create views for CRUD operations
6. ✅ Configure URL routing
7. ✅ Build templates with Django template language
8. ✅ Write and run tests
9. ✅ Run the development server

**Congratulations!** You've built a fully functional Django application. Keep practicing and exploring Django's powerful features!

---

*This tutorial was created for developers transitioning from Python to Django web development. For questions or improvements, please refer to the official Django documentation.*
