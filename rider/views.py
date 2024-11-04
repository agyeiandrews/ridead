from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Rider
from .serializers import RiderSerializer
from rest_framework.permissions import IsAuthenticated

class RiderListView(generics.ListCreateAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]  # Add parser classes for file uploads

    def post(self, request, *args, **kwargs):
        serializer = RiderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate with the authenticated user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        queryset = Rider.objects.all()
        serializer = RiderSerializer(queryset, many=True)
        return Response(serializer.data)


class RiderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        Rider = self.get_object()
        serializer = RiderSerializer(Rider)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        Rider = self.get_object()
        serializer = RiderSerializer(Rider, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        Rider = self.get_object()
        Rider.delete()
        return Response(status=204)


class GenerateQRCodeView(generics.UpdateAPIView):
    queryset = Rider.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        rider = self.get_object()
        qr_data = f"https://yourapp.com/rider/{rider.rider_id}/"  # Replace with your URL pattern
        qr_code_url = generate_qr_code(qr_data)
        rider.qr_code_url = qr_code_url
        rider.save()
        return Response({'qr_code_url': qr_code_url})