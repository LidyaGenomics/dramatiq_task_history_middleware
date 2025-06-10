from rest_framework import serializers
from .models import Pipeline, Task
from datetime import timedelta

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

class PipelineSerializer(serializers.ModelSerializer):
    started_at = serializers.SerializerMethodField()
    completed_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Pipeline
        fields = '__all__'
    
    def get_started_at(self, obj):
        """Return the earliest enqueued_at time from pipeline tasks"""
        earliest_task = obj.task_set.order_by('enqueued_at').first()
        return earliest_task.enqueued_at if earliest_task else None
    
    def get_completed_at(self, obj):
        """Return the latest completed_at time if pipeline status is failed/success"""
        if obj.status in ['failed', 'success']:
            latest_task = obj.task_set.filter(completed_at__isnull=False).order_by('-completed_at').first()
            return latest_task.completed_at if latest_task else None
        return None