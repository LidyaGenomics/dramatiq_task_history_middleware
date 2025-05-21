from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import PipelineViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'pipelines', PipelineViewSet)

# Create a nested router for tasks under pipelines
pipelines_router = routers.NestedDefaultRouter(router, r'pipelines', lookup='pipeline')
pipelines_router.register(r'tasks', TaskViewSet, basename='pipeline-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(pipelines_router.urls)),
] 