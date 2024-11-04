from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated

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
    
        # Add full URL for video field
        for data in serializer.data:
            if 'video' in data and data['video']:  # Check if video is not empty or None
                data['video'] = request.build_absolute_uri(settings.MEDIA_URL + str(data['video']))

        return Response(serializer.data)

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
