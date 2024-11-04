from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.translation import gettext as _
from django.conf import settings
from rest_framework.parsers import JSONParser
from role.models import Role
from role.serializers import RoleSerializer
# Create your views here.


class RoleListView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]  # Add parser classes for file uploads

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)  

    def post(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    
    def get(self, request, *args, **kwargs):
        queryset = Role.objects.all()
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)


class RoleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)