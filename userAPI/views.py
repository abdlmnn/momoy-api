from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model

from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from .serializers import EmailSignupSerializer

from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated

import secrets
from django.conf import settings
from .models import PendingEmailVerification


class TestView(APIView):
  def get(self, request, format=None):
    print("API was called")

    return Response({
      "Message: ": "You made it",
    },status=status.HTTP_200_OK)

User = get_user_model()

class GoogleLoginView(APIView):
    permission_classes = []  # allow unauthenticated POST

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Missing token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try validating against either Web or Android client ID
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                [settings.GOOGLE_CLIENT_ID, settings.GOOGLE_ANDROID_CLIENT_ID]
            )

            email = idinfo.get("email")
            full_name = idinfo.get("name", "")
            google_id = idinfo.get("sub")



            if not email:
                return Response({"error": "No email in token"}, status=status.HTTP_400_BAD_REQUEST)

            # Split full name into first, middle, last
            name_parts = full_name.strip().split()
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # user, created = User.objects.get_or_create(
            #     username=email,
            #     defaults={"email": email, "first_name": first_name,
            #         "last_name": last_name,}
            # )

            user, created = None, False
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create new user if not found
                user = User.objects.create(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True  
                )
                created = True

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "message": "Login successful",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "google_id": google_id,
                "refresh": str(refresh),
                "access": str(access),
                "is_new_user": created,
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": "Invalid token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []  

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"error": "Email not verified"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "message": "Login successful",
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "refresh": str(refresh),
            "access": str(access),
        }, status=status.HTTP_200_OK)

class EmailSignupView(APIView):
    permission_classes = []  # allow unauthenticated POST

    def post(self, request):
        serializer = EmailSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        # Check if user already exists
        # if User.objects.filter(email=email).exists():
        #     return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create inactive user
        # user = User.objects.create_user(
        #     username=email,
        #     email=email,
        #     is_active=False
        # )

        # Generate verification token
        # token = default_token_generator.make_token(user)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build verification URL
        # current_site = get_current_site(request)
        # verification_link = f"http://{current_site.domain}/auth/verify-email/{uid}/{token}/"

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if PendingEmailVerification.objects.filter(email=email).exists():
            return Response({"error": "Email already pending verification"}, status=status.HTTP_400_BAD_REQUEST)

        token = secrets.token_urlsafe(32)

        PendingEmailVerification.objects.create(email=email, token=token)

        verification_link = f"http://{request.get_host()}/auth/verify-email/?token={token}"


        # Send email
        send_mail(
            subject="Verify your email",
            message=f"Click this link to verify your account: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,  # will raise error if SMTP fails
        )

        return Response({"message": "Check your email to verify your account"}, status=status.HTTP_201_CREATED)

class VerifyEmailView(APIView):
    permission_classes = []
    
    def get(self, request):
        token = request.query_params.get("token")

        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pending = PendingEmailVerification.objects.get(token=token)
        except PendingEmailVerification.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=pending.email).exists():
            return Response({"error": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=pending.email,
            email=pending.email,
            is_active=True
        )

        pending.delete()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Email verified successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
        }, status=status.HTTP_200_OK)
    
    # def get(self, request, uidb64, token):
        # try:
        #     uid = force_bytes(urlsafe_base64_decode(uidb64))
        #     user = User.objects.get(pk=uid)
        # except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        #     return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        # if default_token_generator.check_token(user, token):
        #     user.is_active = True
        #     user.save()

        #     refresh = RefreshToken.for_user(user)
        #     access = str(refresh.access_token)
        #     refresh_token = str(refresh)

        #     return Response({"message": "Email verified successfully", "access": access,
        #         "refresh": refresh_token,
        #         "email": user.email,}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class CheckVerificationView(APIView):
    permission_classes = []

    def get(self, request):
        email = request.query_params.get("email")

        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "This email has not been verified yet"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "email": user.email,
            "is_verified": user.is_active,
        }

        if user.is_active:
            refresh = RefreshToken.for_user(user)
            data["access"] = str(refresh.access_token)
            data["refresh"] = str(refresh)

        return Response({"data": data}, status=status.HTTP_200_OK)

class CreateAccountView(APIView):
    permission_classes = [IsAuthenticated]  # [IsAuthenticated] Require JWT (user already logged in after email verification)

    def post(self, request):
        first_name = request.data.get("first_name", "").strip()
        last_name = request.data.get("last_name", "").strip()
        phone = request.data.get("phone", "").strip()
        password = request.data.get("password", "").strip()

        # Validate
        if not first_name or not last_name or not phone:
            return Response({"error": "First name, last name, and phone are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not phone.isdigit() or len(phone) != 10:
            return Response({"error": "Phone must be exactly 10 digits"},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone=phone).exclude(id=request.user.id).exists():
            return Response({"error": "Phone already in use"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update user
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone

        if password:
            if len(password) < 8:
                return Response({"error": "Password must be at least 8 characters"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)

        user.save()

        return Response({
            "message": "Congrats nalang!!!",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "password": bool(password),
        }, status=status.HTTP_200_OK)