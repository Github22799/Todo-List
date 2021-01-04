from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return todos(request)


def todos(request):
    todos_list = []
    return render(request, 'todo/todos.html', {'titile': 'Todos', 'todos': todos_list})


def completed(request):
    return todos(request)
