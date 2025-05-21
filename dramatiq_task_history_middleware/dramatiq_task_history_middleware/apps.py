from django.apps import AppConfig


class DramatiqTaskHistoryMiddlewareConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dramatiq_task_history_middleware'
    verbose_name = 'Dramatiq Task History Middleware'
