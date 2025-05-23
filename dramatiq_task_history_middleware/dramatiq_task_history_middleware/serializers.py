from rest_framework import serializers
from .models import Pipeline, Task
from datetime import timedelta

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class PipelineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pipeline
        fields = '__all__'