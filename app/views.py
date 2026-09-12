from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from app.tasks import calculate_cost_task
from app.models import *


def login(request):
    return render(request, 'customer/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def auth_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/manage/')
    else:
        return render(request, 'customer/login_failed.html')


def registration(request):
    return render(request, 'customer/registration.html')


def confirm_registration(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    try:
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
    except:
        return render(request, 'customer/registration_error.html')
    return render(request, 'customer/registered.html')


@login_required
def manage(request):
    bike_list = []
    try:
        bikes = Bike.objects.filter(is_available=True)
    except:
        bikes = None
    if bikes is not None:
        for bike in bikes:
            bike_dictionary = {'id': bike.bike_id, 'model': bike.bike_model, 'type': bike.bike_type,
                               'cost': bike.bike_cost,
                               'is_available': bike.is_available}
            bike_list.append(bike_dictionary)
    return render(request, 'customer/manage.html', {'bike_list': bike_list})


@login_required
def rent_bike(request):
    bike_id = request.POST['bike_id']
    bike = Bike.objects.get(bike_id=bike_id)
    return render(request, 'customer/confirmation.html', {'bike': bike})


@login_required
def rent_failed(request):
    return render(request, 'customer/rent_failed.html')


@login_required
def confirm_rental(request):
    bike_id = request.POST['bike_id']
    bike = Bike.objects.get(bike_id=bike_id)
    user = User.objects.get(id=request.user.id)
    try:
        Rental.objects.get(user_id=user.id, status="Active")
        return render(request, 'customer/rent_failed.html')
    except:
        if bike.is_available:
            rental = Rental(bike=bike, user=user, status='Active')
            rental.save()
            bike.is_available = False
            bike.save()
            return render(request, 'customer/confirm_rental.html', {'bike': bike})
        else:
            return render(request, 'customer/rent_failed.html')


@login_required
def get_rental_info(request):
    history = []
    rentals = Rental.objects.filter(user_id=request.user.id, status='Ended')
    for rental in rentals:
        history.append(rental)
    try:
        active_rental = Rental.objects.get(user_id=request.user.id, status='Active')
        bike = Bike.objects.get(bike_id=active_rental.bike_id)
        return render(request, 'customer/user_rental_info.html',
                      {'rental': active_rental, 'bike': bike, 'history': history})
    except:
        return render(request, 'customer/user_rental_info.html', {'history': history})


@login_required
def end_rental(request):
    # try:
        rental_id = request.POST['id']
        rental = Rental.objects.get(id=rental_id)
        bike = Bike.objects.get(bike_id=rental.bike_id)
        rental.end_time = timezone.now()
        rental.save()
        result = calculate_cost_task.delay(rental.id)
        rental.status = 'Ended'
        [rental.cost, rental.duration] = result.get()
        rental.save()
        bike.is_available = True
        bike.save()
        return render(request, 'customer/end_rent.html', {'cost': rental.cost, 'duration': rental.duration})
    # except:
    #     return HttpResponseRedirect('/get_rental_info/')


@login_required
def delete_rental(request):
    rental_id = request.POST['id']
    rental = Rental.objects.get(id=rental_id)
    rental.delete()
    return HttpResponseRedirect('/get_rental_info/')
