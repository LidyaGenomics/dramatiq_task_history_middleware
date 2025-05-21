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
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        tasks = self.task_set.all()
        if not tasks.exists():
            return 'processing'
            
        # Check if any tasks are still processing
        if tasks.filter(state__in=['enqueued', 'started']).exists():
            return 'processing'
            
        # Check if any tasks failed
        if tasks.filter(state='failed').exists():
            return 'failed'
            
        # If all tasks are completed
        return 'success'

class Task(models.Model):
    id = models.UUIDField(primary_key=True)
    queue_name = models.CharField(max_length=255)
    actor_name = models.CharField(max_length=255)
    message_json = models.JSONField()
    
    enqueued_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    state = models.CharField(max_length=255, choices=[('enqueued', 'Enqueued'), ('started', 'Started'), ('completed', 'Completed'), ('failed', 'Failed')])
    
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    
