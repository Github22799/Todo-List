from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from todo.models import Todo
from .serializers import TodosSerializer, TodosIDOnlySerializer


class TodosViewerCommon:
    serializer_class = TodosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class TodosViewer(TodosViewerCommon, generics.ListCreateAPIView):
    def get_queryset(self):
        return Todo.objects \
            .filter(user=self.request.user, **self.filter_args())


class PendingTodosViewer(TodosViewer):

    def filter_args(self):
        return {'date_completed__isnull': True}

    def get_queryset(self):
        return super().get_queryset().order_by('-date_created')


class CompletedTodosViewer(TodosViewer):

    def filter_args(self):
        return {'date_completed__isnull': False}

    def get_queryset(self):
        return super().get_queryset().order_by('-date_completed')


class SingleTodoViewer(TodosViewerCommon, generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Todo.objects \
            .filter(user=self.request.user, id=self.kwargs['pk'])


class DateCompletedTodoEditBase(generics.UpdateAPIView):
    serializer_class = TodosIDOnlySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        todo = Todo.objects.get(id=self.kwargs['pk'])
        if self.not_valid(todo):
            raise ValidationError(self.error_message)
        self.set_date_completed(serializer)
        serializer.save()


class CompleteTodoViewer(DateCompletedTodoEditBase):
    error_message = "The todo is already completed."

    def not_valid(self, todo):
        return todo.date_completed is not None

    def set_date_completed(self, serializer):
        serializer.instance.date_completed = timezone.now()


class UncompleteTodoViewer(DateCompletedTodoEditBase):
    error_message = "The todo is not completed yet."

    def not_valid(self, todo):
        return todo.date_completed is None

    def set_date_completed(self, serializer):
        serializer.instance.date_completed = None


def create_token(user):
    return Token.objects.create(user=user)


def get_token_response(token):
    return JsonResponse({'token': str(token)}, status=200)


@csrf_exempt
def signin(request):  # returns a token
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'The username and the password didn\'t match. please try again.'}, status=400)
        login(request, user)
        try:
            token = Token.objects.get(user=user)
        except:
            token = create_token(user)

        return get_token_response(token)


@csrf_exempt
def signup(request):  # creates a user and returns a token
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            return get_token_response(create_token(user))
        except IntegrityError:
            return JsonResponse({'error': 'A user with the same username already exists. please try another one.'})
