from rest_framework import generics, permissions
from todo.models import Todo
from .serializers import TodosSerializer


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
