from rest_framework import serializers
from .models import Pipeline, Task
from datetime import timedelta

class TaskSerializer(serializers.ModelSerializer):
    queue_time = serializers.SerializerMethodField()
    processing_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_queue_time(self, obj):
        if obj.started_at and obj.enqueued_at:
            return (obj.started_at - obj.enqueued_at).total_seconds()
        return None

    def get_processing_time(self, obj):
        if obj.completed_at and obj.started_at:
            return (obj.completed_at - obj.started_at).total_seconds()
        return None

class PipelineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pipeline
        fields = '__all__'