from django.db import models

class Pipeline(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('failed', 'Failed'),
        ('success', 'Success')
    ]

    id = models.UUIDField(primary_key=True)
    
    organization_id = models.UUIDField()
    organization_name = models.CharField(max_length=255)
    
    person_id = models.UUIDField()
    person_name = models.CharField(max_length=255)
    
    file_name_1 = models.CharField(max_length=255, null=True, blank=True)
    file_name_2 = models.CharField(max_length=255, null=True, blank=True)
    
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    id = models.UUIDField(primary_key=True)
    queue_name = models.CharField(max_length=255)
    actor_name = models.CharField(max_length=255)
    message_json = models.JSONField()
    
    enqueued_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    queue_time = models.IntegerField(null=True, blank=True)
    processing_time = models.IntegerField(null=True, blank=True)
    
    state = models.CharField(max_length=255, choices=[('enqueued', 'Enqueued'), ('started', 'Started'), ('completed', 'Completed'), ('failed', 'Failed')])
    
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    
