from celery import shared_task
from app.models import *


@shared_task
def calculate_cost_task(rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.duration = round((rental.end_time - rental.start_time).total_seconds())
    rental.cost = round(rental.duration / 60 * float(rental.bike.price_per_minute), 2)
    rental.save()
    return rental.cost, rental.duration

