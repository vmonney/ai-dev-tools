# Django TODO Application

A fully-functional TODO application built with Django, featuring CRUD operations, due dates, and completion tracking.

## Features

- ✅ **Create TODOs** - Add new tasks with title, description, and due date
- ✅ **Edit TODOs** - Update existing tasks
- ✅ **Delete TODOs** - Remove completed or unwanted tasks
- ✅ **Mark as Resolved** - Toggle completion status with one click
- ✅ **Due Dates** - Set deadlines and see overdue indicators
- ✅ **Filtering** - View all, active, or completed TODOs
- ✅ **Admin Panel** - Full Django admin integration
- ✅ **Responsive UI** - Clean, modern interface
- ✅ **Comprehensive Tests** - 34 test cases covering all functionality

## Quick Start

### 1. Install uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Set Up Virtual Environment

```bash
uv venv
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run Tests

```bash
python manage.py test
```

### 7. Start Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Project Structure

```
.
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── HOMEWORK_ANSWERS.md      # Answers to homework questions
├── DJANGO_TUTORIAL.md       # Comprehensive tutorial
├── todoproject/             # Django project configuration
│   ├── settings.py          # Project settings
│   └── urls.py              # Main URL configuration
└── todos/                   # TODO application
    ├── models.py            # Todo model
    ├── views.py             # CRUD views
    ├── urls.py              # App URL patterns
    ├── admin.py             # Admin configuration
    ├── tests.py             # Test cases (34 tests)
    └── templates/           # HTML templates
        └── todos/
            ├── base.html
            ├── home.html
            ├── todo_form.html
            └── todo_confirm_delete.html
```

## Technology Stack

- **Django 5.2.8** - Web framework
- **Python 3.12+** - Programming language
- **SQLite** - Database (development)
- **uv** - Fast Python package manager
- **Django Test Framework** - Testing

## Documentation
- **DJANGO_TUTORIAL.md** - Step-by-step tutorial for building the app from scratch

## Development

### Running Tests

```bash
python manage.py test
```

All 34 tests should pass:
```
Found 34 test(s).
...................................
Ran 34 tests in 0.XXXs
OK
```

### Creating New Migrations

If you modify the models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Managing the Database

```bash
# Open Django shell
python manage.py shell

# Example: Create a TODO
from todos.models import Todo
from datetime import date, timedelta

todo = Todo.objects.create(
    title="My First TODO",
    description="This is a test",
    due_date=date.today() + timedelta(days=7)
)
```

## Usage

### Creating a TODO

1. Click "New TODO" button
2. Fill in title (required), description, and due date
3. Click "Create TODO"

### Editing a TODO

1. Click "Edit" button on any TODO
2. Modify fields as needed
3. Optionally mark as completed
4. Click "Update TODO"

### Deleting a TODO

1. Click "Delete" button on any TODO
2. Confirm deletion

### Marking as Complete

- Click the checkbox next to any TODO to toggle its completion status
- Completed TODOs appear with strikethrough text

### Filtering

- **All** - Show all TODOs
- **Active** - Show only incomplete TODOs
- **Completed** - Show only completed TODOs

## License

This project was created for educational purposes.

## Author

Built with Django by following best practices and the MTV architecture pattern.
