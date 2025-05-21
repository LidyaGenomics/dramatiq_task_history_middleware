from rest_framework import serializers
from .models import Pipeline, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class PipelineSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Pipeline
        fields = [
            'id',
            'organization_id',
            'organization_name',
            'person_id',
            'person_name',
            'file_name_1',
            'file_name_2',
            'created_at',
            'status',
        ] 