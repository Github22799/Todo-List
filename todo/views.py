from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Todo
from django.utils import timezone


def home(request):
    return todos(request)


def todos(request):
    todos_list = [
        Todo(
            pk=0,
            title='test title',
            memo='hello there this is a dummy text.',
            date_created=timezone.now(),
            is_important=False
        ),
        Todo(
            pk=1,
            title='test title',
            memo='hello there this is a dummy text.',
            date_created=timezone.now(),
            is_important=False
        ),
    ]
    return render(request, 'todo/todos.html', {'titile': 'Todos', 'todos': todos_list})


def completed(request):
    return todos(request)


def sign_up(request):
    pass


def sign_in(request):
    pass


def sign_out(request):
    pass
