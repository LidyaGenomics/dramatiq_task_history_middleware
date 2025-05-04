from django.db import models

class Task(models.Model):
    id = models.UUIDField(primary_key=True)
    queue_name = models.CharField(max_length=255)
    actor_name = models.CharField(max_length=255)
    message_json = models.JSONField()
    
    enqueued_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    state = models.CharField(max_length=255, choices=[('enqueued', 'Enqueued'), ('started', 'Started'), ('completed', 'Completed'), ('failed', 'Failed')])