from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .models import Driver
from .serializers import DriverSerializer

class DriverListView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Add parser classes for file uploads

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
    lookup_field = 'id'
    serializer_class = DriverSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            # If 'ad_link' field is not present in the request data,
            # remove it from the validated data to prevent overwriting the existing ad_link
            # if 'ad_link' not in request.data:
            #     serializer.validated_data.pop('ad_link', None)

             # Explicitly update the 'updated_at' field to the current time
            serializer.validated_data['updated_at'] = timezone.now()

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
