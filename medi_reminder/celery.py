"""
Celery configuration for MediReminder project.

This module configures Celery for asynchronous task processing.
It sets up the Celery app with Redis as the message broker and result backend.
"""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medi_reminder.settings')

# Create the Celery app instance
app = Celery('medi_reminder')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Optional: Configure periodic tasks (beat schedule)
app.conf.beat_schedule = {
    # Example: Send reminder notifications every minute
    # 'send-reminders': {
    #     'task': 'reminders.tasks.send_reminder_notifications',
    #     'schedule': 60.0,  # Run every 60 seconds
    # },
}

# Optional: Set timezone
app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup."""
    print(f'Request: {self.request!r}')
