from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from .models import Pipeline, Task
from .serializers import PipelineSerializer, TaskSerializer

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PipelineFilter(filters.FilterSet):
    organization_id = filters.UUIDFilter()
    person_id = filters.UUIDFilter()
    created_at_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Pipeline
        fields = ['organization_id', 'person_id', 'created_at']

class TaskFilter(filters.FilterSet):
    queue_name = filters.CharFilter(lookup_expr='icontains')
    actor_name = filters.CharFilter(lookup_expr='icontains')
    state = filters.CharFilter()
    
    enqueued_at_after = filters.DateTimeFilter(field_name='enqueued_at', lookup_expr='gte')
    enqueued_at_before = filters.DateTimeFilter(field_name='enqueued_at', lookup_expr='lte')
    started_at_after = filters.DateTimeFilter(field_name='started_at', lookup_expr='gte')
    started_at_before = filters.DateTimeFilter(field_name='started_at', lookup_expr='lte')
    completed_at_after = filters.DateTimeFilter(field_name='completed_at', lookup_expr='gte')
    completed_at_before = filters.DateTimeFilter(field_name='completed_at', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['queue_name', 'actor_name', 'state', 'enqueued_at', 'started_at', 'completed_at']

class PipelineViewSet(viewsets.ModelViewSet):
    queryset = Pipeline.objects.all().order_by('-created_at')
    serializer_class = PipelineSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = PipelineFilter

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = TaskFilter

    def get_queryset(self):
        pipeline_id = self.kwargs.get('pipeline_pk')
        if pipeline_id:
            return Task.objects.filter(pipeline_id=pipeline_id).order_by('-enqueued_at')
        return Task.objects.none()
