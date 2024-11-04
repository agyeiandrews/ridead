from django.urls import path
from .views import *

urlpatterns = [
    path('roles', RoleListView.as_view(), name='role-list'),
    path('roles/<uuid:id>', RoleView.as_view(), name='role-detail'),
]
 