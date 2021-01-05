from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm


# TODO this file needs some refactoring.

def home(request):
    if request.user.is_authenticated:
        return todos(request)
    return homepage(request)


def homepage(request):
    return render(request, 'todo/homepage.html', {'title': 'Home Page'})


# TODO make a decorator instead of returning this function.
# TODO you might use the "login_required" decorator instead.
def need_signin_first(request, signin_next):
    context = {
        'title': 'Sign In',
        'form': AuthenticationForm(),
        'error_message': 'You need to sign in first.'
    }
    request.session['signin_next'] = signin_next
    return render(request, 'todo/signin.html', context)


# TODO most of the code in "todos" and "completed" is duplicated.

def todos(request):
    if request.user.is_authenticated:
        request.session['prev_page'] = 'todos'
        todos_list = Todo.objects.filter(user=request.user, date_completed__isnull=True).order_by('-date_created')
        return render(request, 'todo/todos.html', {'title': 'Todos', 'todos': todos_list})
    return need_signin_first(request, 'todos')


def completed(request):
    if request.user.is_authenticated:
        request.session['prev_page'] = 'completed'
        todos_list = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_created')
        return render(request, 'todo/completed.html', {'title': 'Completed', 'todos': todos_list})
    return need_signin_first(request, 'completed')


def switch_GET_POST(request, get_func, post_func):
    if request.method == 'GET':
        return get_func(request)
    else:
        return post_func(request)


def signup_GET(request):
    context = {'title': 'Sign Up', 'form': UserCreationForm()}
    return render(request, 'todo/signup.html', context)


def signup_POST(request):
    form = UserCreationForm(request.POST)

    password1 = request.POST['password1']
    password2 = request.POST['password2']

    # TODO is this enough? may return different messages.
    if password1 == password2 and not form.errors:
        user = form.save()
        login(request, user)
        return redirect('home')
    else:
        context = {
            'title': 'Sign Up',
            'form': form,
            'error_message': 'The two passwords does not match. Please Try again.'
        }
        return render(request, 'todo/signup.html', context)


def signup(request):
    return switch_GET_POST(request, signup_GET, signup_POST)


def signin_GET(request):
    context = {'title': 'Sign In', 'form': AuthenticationForm()}
    return render(request, 'todo/signin.html', context)


def signin_POST(request):
    form = AuthenticationForm(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    # TODO is this enough? may return different messages.
    if user is None or form.errors:
        context = {
            'title': 'Sign In',
            'form': form,
            'error_message': 'The username and the password didn\'t match. Please Try again.'
        }
        return render(request, 'todo/signin.html', context)

    login(request, user)
    return redirect_next_page(request, 'signin_next')


def redirect_next_page(request, key, default_view='home'):
    if key in request.session:
        next_page = request.session[key]
        request.session.delete(key)
        return redirect(next_page)
    return redirect(default_view)


def signin(request):
    return switch_GET_POST(request, signin_GET, signin_POST)


def signout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'is_important']


def create_GET(request):
    context = {'title': 'Create a new Todo!', 'form': TodoForm}
    return render(request, 'todo/create.html', context)


def return_error_message(request, form, page):
    # TODO add a title
    context = {
        'form': form,
        'error_message': 'There was an error processing the given data. Please try again.'
    }
    return render(request, page, context)


def create_POST(request):
    form = TodoForm(request.POST)
    if form.errors:
        return return_error_message(request, form, 'todo/create.html')
    todo = form.save(commit=False)
    todo.user = request.user
    todo.save()
    return redirect('todos')


def create(request):
    if request.user.is_authenticated:
        return switch_GET_POST(request, create_GET, create_POST)
    return need_signin_first(request, 'create')


# TODO you might use a decorator for the functions that redirects
# TODO to the home if the request method isn't a POST request.

def edit_GET(request, todo):
    form = TodoForm(instance=todo)
    context = {'title': 'Edit ' + todo.title, 'form': form}
    return render(request, 'todo/edit.html', context)


def edit_POST(request, todo):
    form = TodoForm(request.POST, instance=todo)

    if form.errors:
        return return_error_message(request, form, 'todo/edit.html')

    form.save()
    return redirect_next_page(request, 'prev_page', 'todos')


def edit(request, pk):
    # TODO you may use something like the "switch_GET_POST" function.
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'GET':
        return edit_GET(request, todo)
    else:
        return edit_POST(request, todo)


def delete(request, pk):
    if request.method == "POST":
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.delete()
    return redirect_next_page(request, 'prev_page', 'todos')


def complete(request, pk):
    if request.method == "POST":
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.date_completed = timezone.now()
        todo.save()
    return redirect_next_page(request, 'prev_page', 'todos')


def uncomplete(request, pk):
    if request.method == "POST":
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        todo.date_completed = None
        todo.save()
    return redirect_next_page(request, 'prev_page', 'completed')
