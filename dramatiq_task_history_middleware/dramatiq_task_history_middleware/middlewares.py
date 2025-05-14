"""
This middleware is used to log state changes and the history of all messages with dramatiq.
1. It logs the message when it's enqueued.
2. It logs the message before it's processed.
3. It logs the message after it's processed.
4. It logs the message when it's completed.
"""

import logging
import datetime
import dramatiq
import pytz

from dramatiq.middleware import Middleware


logger = logging.getLogger(__name__)


class TaskHistoryMiddleware(Middleware):
    """Middleware that logs all messages received by actors."""
    
    def before_enqueue(self, broker, message, delay):
        # Add your custom options here
        message.options["my_custom_option"] = "my_custom_value"
        
        # You can also access other message attributes if needed
        # For example, to add an option based on the actor name:
        # message.options[f"{message.actor_name}_processed"] = False

        return super().before_enqueue(broker, message, delay)

    def after_enqueue(self, broker, message: dramatiq.Message, delay):
        from .models import Task

        
        logger.info(
            "Enqueued message for actor %s with args %s and kwargs %s",
            message.actor_name,
            message.args,
            message.kwargs
        )

        Task.objects.create(
            id=message.options.get("redis_message_id"),
            queue_name=message.queue_name,
            actor_name=message.actor_name,
            message_json=message.asdict(),
            enqueued_at=datetime.datetime.now(pytz.timezone('Europe/Istanbul')),
            state="enqueued"
        )

        return message

    def before_process_message(self, broker, message: dramatiq.Message):
        from .models import Task
        
        """Log the message before it's processed."""
        logger.info(
            "Received message for actor %s with args %s and kwargs %s",
            message.actor_name,
            message.args,
            message.kwargs
        )

        task = Task.objects.get(id=message.options.get("redis_message_id"))
        task.started_at = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
        task.status = "started"
        task.save()
        return message
    
    def after_process_message(self, broker, message: dramatiq.Message, *, result=None, exception=None):
        from .models import Task
        
        """Log the message after it's processed."""
        if exception:
            logger.error(
                "Error processing message for actor %s: %s",
                message.actor_name,
                str(exception)
            )
            task = Task.objects.get(id=message.options.get("redis_message_id"))
            task.state = "failed"
            task.completed_at = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
            task.save()
        else:
            logger.info(
                "Successfully processed message for actor %s",
                message.actor_name
            )
            task = Task.objects.get(id=message.options.get("redis_message_id"))
            task.state = "completed"
            task.completed_at = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
            task.save()
        return message 