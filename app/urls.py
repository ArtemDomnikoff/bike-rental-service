from app.views import *
from django.urls import path

urlpatterns = [
    path(r'', login),
    path(r'auth/', auth_user),
    path(r'logout_user/', logout_user),
    path(r'registration/', registration),
    path(r'confirm_registration/', confirm_registration),
    path(r'get_rental_info/', get_rental_info),
    path(r'end_rental/', end_rental),
    path(r'rent_failed/', rent_failed),
    path(r'rent_bike/', rent_bike),
    path(r'confirm_rental/', confirm_rental),
    path(r'manage/', manage),
    path(r'delete_rental/', delete_rental),
]
