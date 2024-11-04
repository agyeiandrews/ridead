from django.urls import path
from .views import *

urlpatterns = [
    path('riders', RiderListView.as_view(), name='rider-list'),
    path('riders/<uuid:id>', RiderView.as_view(), name='rider-detail'),
    path('rider/generate_qr/<uuid:pk>/', GenerateQRCodeView.as_view(), name='generate_qr_code'),
]
 