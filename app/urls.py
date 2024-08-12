from app.views import *
from django.urls import path

urlpatterns = [
    path(r'', login),
    path(r'auth/', auth_view),
    path(r'logout/', logout_view),
    path(r'register/', register),
    path(r'registration/', registration),
    path(r'active_rental/', active_rental),
    path(r'end_rental/', end_rental),
    path(r'rent_failed/', rent_failed),
    path(r'rent/', rent_vehicle),
    path(r'confirmed/', confirm),
    path(r'manage/', manage),
    path(r'delete/', delete),
]
