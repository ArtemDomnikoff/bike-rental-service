import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bike-rental-service.settings')
app = Celery('bike-rental-service',broker="redis://localhost:6379")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
