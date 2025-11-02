import json

def create_periodic_tasks(sender, **kwargs):
    """Create or update periodic Celery Beat tasks after migrations."""
    from django_celery_beat.models import PeriodicTask, CrontabSchedule
    try:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='*',
            day_of_week='1,2,3,4,5',
            timezone='America/Sao_Paulo',
        )

        PeriodicTask.objects.update_or_create(
            name='save_news_periodic_task',
            defaults={
                'task': 'core.tasks.save_news',
                'crontab': schedule,
                'args': json.dumps([]),
                'enabled': True,
            },
        )

        print("✅ Periodic task 'save_news_periodic_task' created or updated successfully.")
    except Exception as e:
        print(f"⚠️ Could not create periodic task: {e}")