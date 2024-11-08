from django.urls import reverse
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from user.authentication import PhoneNumberBackend
from .models import User, UserProfile
from .serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer, UserProfileSerializer, UserSerializer
from django.contrib.auth import authenticate, logout
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__id'  # Use user ID to look up the profile
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return self.queryset.filter(user__id=user_id)
    
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
    
        # Add full URL for icon field
        for data in serializer.data:
            if 'profile_picture' in data and data['profile_picture']:  # Check if icon is not empty or None
                data['profile_picture'] = request.build_absolute_uri(settings.MEDIA_URL + str(data['profile_picture']))

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            # If 'profile_picture' field is not present in the request data,
            # remove it from the validated data to prevent overwriting the existing profile_picture
            if 'profile_picture' not in request.data:
                serializer.validated_data.pop('profile_picture', None)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [PhoneNumberBackend]
    def post(self, request):
        try:
            # Get username and password from request data
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')

            # Check if both phone_number and password are provided
            if not phone_number or not password:
                raise ValidationError("Phone Number or password is missing")

            # Authenticate user
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                # Generate or retrieve token
                refresh = RefreshToken.for_user(user)
                # Retrieve user details
                user_serializer = UserSerializer(user)
                return Response({
                    'user': user_serializer.data,
                    'token': str(refresh.access_token),
                })
            else:
                raise AuthenticationFailed('Invalid credentials')
        except ValidationError as e:
            # Log validation error for debugging purposes
            print(f"Validation error during login: {str(e)}")
            # Return a more informative error response
            raise APIException("Invalid request data")
        except AuthenticationFailed as e:
            # Log authentication error for debugging purposes
            print(f"Authentication failed during login: {str(e)}")
            # Return a more informative error response
            raise APIException("Invalid credentials")
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred during login: {str(e)}")
            # Return a more informative error response
            raise APIException("Internal server error occurred during login")

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse({'success': 'Logged out successfully'})

class UserAPIView(APIView):
    def get(self, request):
        user = request.user
        return JsonResponse({'username': user.username})



##############
#password reset views

# Forgot Password
class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate token and uid for the user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        frontend_url = settings.FRONTEND_URL
        reset_link = request.build_absolute_uri(f'{frontend_url}/reset-password/{uid}/{token}')

        context = {
            'user': user,
            'reset_link': reset_link,
        }

        subject = 'Password Reset Request'
        message = render_to_string('password_reset_email.html', context)
        
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(
                subject,
                '',
                email_from,
                recipient_list,
                html_message=message,
                fail_silently=False
            )
            return JsonResponse({'message': 'Password reset instructions sent to your email.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error sending email: {e}")
            return JsonResponse({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Password Reset Confirm
class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        data = request.data
        serializer = PasswordResetConfirmSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        password = data.get('new_password')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'success': 'Password has been reset'}, status=status.HTTP_200_OK)