from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Driver
from .serializers import DriverSerializer

class DriverListView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]  # Add parser classes for file uploads

    def post(self, request, *args, **kwargs):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate with the authenticated user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        queryset = Driver.objects.all()
        serializer = DriverSerializer(queryset, many=True)
        return Response(serializer.data)


class DriverView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        driver = self.get_object()
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, *args, **kwargs):
        driver = self.get_object()
        driver.delete()
        return Response(status=204)
