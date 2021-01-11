from rest_framework import serializers
from todo.models import Todo


class TodosSerializer(serializers.ModelSerializer):
    date_created = serializers.ReadOnlyField()

    def to_representation(self, instance):
        ret = super(TodosSerializer, self).to_representation(instance)
        if instance.date_completed:
            ret['date_completed'] = instance.date_completed
        return ret

    class Meta:
        model = Todo
        fields = ['id', 'title', 'memo', 'date_created', 'is_important']
