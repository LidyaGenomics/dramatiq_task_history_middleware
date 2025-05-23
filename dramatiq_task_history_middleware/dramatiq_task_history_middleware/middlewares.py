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

from dramatiq.middleware import Middleware, CurrentMessage


logger = logging.getLogger(__name__)


class TaskHistoryMiddleware(Middleware):
    """Middleware that logs all messages received by actors."""
    
    def before_enqueue(self, broker, message: dramatiq.Message, delay):
        current_message = CurrentMessage.get_current_message()
        
        if not current_message:
            # initial message stem from the backend
            from .models import Pipeline
            import uuid
            
            organization_id = message.options.get("options", {}).get("organization_id")
            
            if not organization_id:
                logger.info("No organization_id found in message options. Probably not a pipeline processing message.")
                return message
            
            organization_name = message.options.get("options", {}).get("organization_name")
            
            person_id = message.options.get("options", {}).get("person_id")
            person_name = message.options.get("options", {}).get("person_name")
            
            file_name_1 = message.options.get("options", {}).get("file_name_1") 
            file_name_2 = message.options.get("options", {}).get("file_name_2")
            
            # generate a random uuid for the pipeline
            pipeline_id = str(uuid.uuid4())
            
            pipeline = Pipeline.objects.create(
                id=pipeline_id,
                organization_id=organization_id,
                organization_name=organization_name,
                person_id=person_id,
                person_name=person_name,
                file_name_1=file_name_1,
                file_name_2=file_name_2,
            )
            
            # merge current_message.options with message.options
            if "options" not in message.options:
                message.options["options"] = {}

            message.options["options"]["pipeline_id"] = pipeline.id
        else:
            # intermediate message stem from the worker
            pipeline_id = current_message.options.get("options", {}).get("pipeline_id")

            if not pipeline_id:
                logger.info("No pipeline_id or organization_id found in message options")
                return message
            
            if "options" not in message.options:
                message.options["options"] = {}
            message.options["options"]["pipeline_id"] = pipeline_id
                
        return message

    def after_enqueue(self, broker, message: dramatiq.Message, delay):
        from .models import Task

        
        logger.info(
            "Enqueued message for actor %s with args %s and kwargs %s",
            message.actor_name,
            message.args,
            message.kwargs
        )
        
        from .models import Pipeline
        pipeline_id = message.options.get("options", {}).get("pipeline_id")
        
        if not pipeline_id:
            logger.info("No pipeline_id found in message options. Probably not a pipeline processing message.")
            return message
        
        pipeline = Pipeline.objects.get(id=pipeline_id)
        
        Task.objects.create(
            id=message.options.get("redis_message_id"),
            queue_name=message.queue_name,
            actor_name=message.actor_name,
            message_json=message.asdict(),
            enqueued_at=datetime.datetime.now(pytz.timezone('Europe/Istanbul')),
            state="enqueued",
            pipeline=pipeline
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

        task = Task.objects.filter(id=message.options.get("redis_message_id")).first()
        
        if not task:
            logger.info("No task found for message. Probably not a pipeline processing message.")
            return message
        
        task.started_at = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
        task.queue_time = (task.started_at - task.enqueued_at).total_seconds() * 1000
        task.state = "started"
        task.save()
        return message
    
    def after_process_message(self, broker, message: dramatiq.Message, *, result=None, exception=None):
        from .models import Task, Pipeline
        
        organization_id = message.options.get("options", {}).get("organization_id")
        pipeline_id = message.options.get("options", {}).get("pipeline_id")
        is_pipeline_start_task = False
        if organization_id and pipeline_id:
            is_pipeline_start_task = True
            logger.info(
                "Organization ID: %s, Pipeline ID: %s",
                organization_id,
                pipeline_id
            )
        
        """Log the message after it's processed."""
        if exception:
            logger.error(
                "Error processing message for actor %s: %s",
                message.actor_name,
                str(exception)
            )
            task = Task.objects.filter(id=message.options.get("redis_message_id")).first()
            
            if not task:
                logger.info("Failed to process message. No task found for message. Probably not a pipeline processing message.")
                return message
            
            task.state = "failed"
            task.completed_at = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
            task.processing_time = (task.completed_at - task.started_at).total_seconds() * 1000
            task.save()
            
            if is_pipeline_start_task:
                pipeline = Pipeline.objects.get(id=pipeline_id)
                pipeline.status = "failed"
                pipeline.save()
        else:
            logger.info(
                "Successfully processed message for actor %s",
                message.actor_name
            )
            task = Task.objects.filter(id=message.options.get("redis_message_id")).first()
            
            if not task:
                logger.info("Successfully processed message. No task found for message. Probably not a pipeline processing message.")
                return message
            
            task.state = "completed"
            task.completed_at = datetime.datetime.now(pytz.timezone('Europe/Istanbul'))
            task.processing_time = (task.completed_at - task.started_at).total_seconds() * 1000
            task.save()
            
            if is_pipeline_start_task:
                pipeline = Pipeline.objects.get(id=pipeline_id)
                pipeline.status = "success"
                pipeline.save()
        return message 