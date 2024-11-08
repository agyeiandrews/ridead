from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from ads.serializers import AdSerializer
from .models import Ad, AdInteraction, Reward

class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AdSerializer
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        queryset = Ad.objects.all()
        serializer = AdSerializer(queryset, many=True)
    
        # Add full URL for ad_link field
        for data in serializer.data:
            if 'ad_link' in data and data['ad_link']:  # Check if ad_link is not empty or None
                data['ad_link'] = request.build_absolute_uri(settings.MEDIA_URL + str(data['ad_link']))

        return Response(serializer.data)

class AdView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            # If 'ad_link' field is not present in the request data,
            # remove it from the validated data to prevent overwriting the existing ad_link
            if 'ad_link' not in request.data:
                serializer.validated_data.pop('ad_link', None)

             # Explicitly update the 'updated_on' field to the current time
            serializer.validated_data['updated_on'] = timezone.now()

             # If the user is viewing the ad, increment the view count and add the user to 'viewed_by'
            if 'user_id' in request.data:  # Assuming user ID is passed in the request body
                user_id = request.data.get('user_id')
                user = User.objects.get(id=user_id)  # Find the user
                instance.increment_view_count(user)  # Update the view count and add the user

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdInteractionView(generics.CreateAPIView):
    queryset = AdInteraction.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ad_id = request.data.get('ad_id')
        rider = request.user

        # Create the interaction
        interaction = AdInteraction.objects.create(rider=rider, ad_id=ad_id)

        # Reward logic
        if not interaction.reward_given:
            driver = interaction.ad.driver  # Get the driver associated with the ad
            Reward.objects.create(rider=rider, driver=driver)

            # Mark the interaction as rewarded
            interaction.reward_given = True
            interaction.save()

        return Response({'message': 'Ad viewed and rewards granted!'})
