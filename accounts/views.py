from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, throttle_classes, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.generics import CreateAPIView
from .forms import CustomUserCreationForm
from django.contrib.auth import logout as auth_logout

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Clear all initial data
        for field in form.fields.values():
            field.initial = None
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your account has been created successfully. Please log in.')
        return response
from django.contrib import messages
from .utils import generate_token, send_verification_email, send_password_reset_email
from .serializers import (
    UserSerializer, RegisterSerializer, ChangePasswordSerializer, UserProfileSerializer,
    EmailVerificationSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .models import UserProfile

class AuthRateThrottle(AnonRateThrottle):
    rate = '5/minute'

class APIRegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def perform_create(self, serializer):
        user = serializer.save()
        profile = user.userprofile
        token = generate_token()
        profile.verification_token = token
        profile.verification_token_created = timezone.now()
        profile.save()
        send_verification_email(user, token)

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.initial = None
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. Please log in with your new account.')
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def verify_email(request):
    serializer = EmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        profile = get_object_or_404(UserProfile, verification_token=token)
        
        # Check if token is not expired (24 hours validity)
        if profile.verification_token_created < timezone.now() - timezone.timedelta(hours=24):
            return Response(
                {'error': 'Verification link has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.email_verified = True
        profile.verification_token = ''
        profile.save()
        
        return Response({'message': 'Email verified successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            profile = user.userprofile
            token = generate_token()
            profile.verification_token = token
            profile.verification_token_created = timezone.now()
            profile.save()
            send_password_reset_email(user, token)
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            pass  # Silent fail for security
        
    return Response({'message': 'If the email exists, a reset link has been sent'})

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([AuthRateThrottle])
def reset_password(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        profile = get_object_or_404(UserProfile, verification_token=token)
        
        if profile.verification_token_created < timezone.now() - timezone.timedelta(hours=24):
            return Response(
                {'error': 'Password reset link has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = profile.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        profile.verification_token = ''
        profile.save()
        
        return Response({'message': 'Password reset successful'})

# Allow GET logout to simplify navbar click -> logout behavior
def logout_view(request):
    auth_logout(request)
    return redirect('home')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        
    @action(detail=False, methods=['POST'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def my_profile(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def sync_offline_data(self, request):
        profile = UserProfile.objects.get(user=request.user)
        profile.last_sync_date = timezone.now()
        profile.save()
        return Response({'status': 'sync successful'})
