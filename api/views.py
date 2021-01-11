from rest_framework import generics, permissions
from todo.models import Todo
from .serializers import TodosSerializer, PendingTodosSerializer


class TodosViewer(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return Todo.objects\
            .filter(user=self.request.user, **self.filter_args())\
            .order_by(self.order_args())


class PendingTodosViewer(TodosViewer):
    serializer_class = PendingTodosSerializer

    def filter_args(self):
        return {'date_completed__isnull': True}

    def order_args(self):
        return '-date_created'


class CompletedTodosViewer(TodosViewer):
    serializer_class = TodosSerializer

    def filter_args(self):
        return {'date_completed__isnull': False}

    def order_args(self):
        return '-date_completed'
