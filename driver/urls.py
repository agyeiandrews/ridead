from django.urls import path
from .views import *

urlpatterns = [
    path('drivers', DriverListView.as_view(), name='driver-list'),
    path('drivers/<uuid:id>', DriverView.as_view(), name='driver-detail'),
]