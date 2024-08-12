from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from app.tasks import end_rental_task
from app.models import *


def login(request):
    return render(request, 'customer/login.html')


def auth_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/manage/')
    else:
        return render(request, 'customer/login_failed.html')


def register(request):
    return render(request, 'customer/register.html')


def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
    except:
        return render(request, 'customer/registration_error.html')
    customer = Customer(user=user, email=email, username=username)
    customer.save()
    return render(request, 'customer/registered.html')


def logout_view(request):
    return render(request, 'customer/login.html')


@login_required
def manage(request):
    bike_list = []
    try:
        bikes = Bike.objects.filter(is_available=True)
    except:
        bikes = None
    if bikes is not None:
        for bike in bikes:
            bike_dictionary = {'id': bike.id, 'model': bike.model, 'type': bike.type,
                               'price_per_hour': bike.price_per_hour,
                               'is_available': bike.is_available}
            bike_list.append(bike_dictionary)
    return render(request, 'customer/manage.html', {'bike_list': bike_list})


@login_required
def rent_vehicle(request):
    bike_id = request.POST['bike_id']
    bike = Bike.objects.get(id=bike_id)
    return render(request, 'customer/confirmation.html', {'bike': bike})


@login_required
def rent_failed(request):
    return render(request, 'customer/rent_failed.html')


@login_required
def confirm(request):
    bike_id = request.POST['bike_id']
    bike = Bike.objects.get(id=bike_id)
    customer = Customer.objects.get(user=request.user)
    try:
        Rental.objects.get(user_id=request.user.id, status="Active")
        return render(request, 'customer/rent_failed.html')
    except:
        if bike.is_available:
            rental = Rental(bike=bike, user=customer, status='Active')
            rental.save()
            bike.is_available = False
            bike.save()
            return render(request, 'customer/confirmed.html', {'bike': bike})
        else:
            return render(request, 'customer/rent_failed.html')


@login_required
def active_rental(request):
    history = []
    rentals = Rental.objects.filter(user_id=request.user.id, status='Ended')
    for rental in rentals:
        history.append(rental)
    try:
        rental = Rental.objects.filter(user_id=request.user.id, status="Active")[0]
        bike = Bike.objects.get(id=rental.bike_id)
        return render(request, 'customer/active_rental.html', {'rental': rental, 'bike': bike, 'history': history})
    except:
        return render(request, 'customer/active_rental.html', {'history': history})


@login_required
def end_rental(request):
    rental_id = request.POST['id']
    rental = Rental.objects.get(id=rental_id)
    if rental.end_time is None:
        end_rental_task.delay(rental_id)
        rental.save()
        rental.bike.is_available = True
        rental.bike.save()
        return render(request, 'customer/rental_ended.html')
    else:
        return HttpResponseRedirect('/manage/')


@login_required
def delete(request):
    rental_id = request.POST['id']
    rental = Rental.objects.get(id=rental_id)
    rental.delete()
    return HttpResponseRedirect('/active_rental/')
