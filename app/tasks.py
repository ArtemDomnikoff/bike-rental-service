from celery import shared_task
from django.utils import timezone
from celery import Celery
from app.models import *

app = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')


@shared_task
def end_rental_task(rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.end_time = timezone.now()
    rental.status = 'Ended'
    calculate_cost_task.delay(rental_id)


@shared_task
def calculate_cost_task(rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.duration = (timezone.now() - rental.start_time).total_seconds() / 60
    rental.cost = round(rental.duration * float(rental.bike.price_per_hour), 2)
