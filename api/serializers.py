from rest_framework import serializers
from todo.models import Todo


class TodosSerializer(serializers.ModelSerializer):
    date_created = serializers.ReadOnlyField()
    date_completed = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['title', 'memo', 'date_created', 'date_completed', 'is_important']


class PendingTodosSerializer(TodosSerializer):

    class Meta:
        model = Todo
        fields = ['title', 'memo', 'date_created', 'is_important']
