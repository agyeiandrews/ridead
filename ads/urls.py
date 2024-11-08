from django.urls import path
from .views import AdListView, AdInteractionView, AdView

urlpatterns = [
    path('ads', AdListView.as_view(), name='ad-list'),
    path('ads/<uuid:id>', AdView.as_view(), name='ad-detail'),
    path('ads/interact', AdInteractionView.as_view(), name='ad-interaction'),
]
