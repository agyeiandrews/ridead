from django.urls import path
from .views import AdListView, AdInteractionView

urlpatterns = [
    path('ads', AdListView.as_view(), name='ad-list'),
    path('ads/interact', AdInteractionView.as_view(), name='ad-interaction'),
]
