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

from .serializers import *

from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated

import secrets
from django.conf import settings
from .models import *

from django.core.mail import EmailMultiAlternatives

from django.shortcuts import render

import datetime


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

        # user = authenticate(request, username=email, password=password)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "Email not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user and not user.has_usable_password():
            return Response(
                {"error": "This account does not have a password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # if user is None:
        #     return Response(
        #         {"error": "Invalid credentials"},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )

        if not user.is_active:
            return Response(
                {"error": "Email not verified"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not user.check_password(password):
            return Response(
                {"error": "Incorrect password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Password is correct → issue JWT tokens
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

        # PendingEmailVerification.objects.filter(created_at__lt=timezone.now() - timedelta(hours=1)).delete()
        
        if PendingEmailVerification.objects.filter(email=email).exists():
            return Response({"error": "Email already pending verification"}, status=status.HTTP_400_BAD_REQUEST)

        token = secrets.token_urlsafe(32)

        PendingEmailVerification.objects.create(email=email, token=token)

        verification_link = f"http://{request.get_host()}/auth/verify-email/?token={token}"
        
        subject = "Verify your email"
        text_message = f"Click the link to verify your account: {verification_link}"
        html_message = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <h2>Welcome to Momoy's App!</h2>
            <p>Hi there,</p>
            <p>Please verify your email address by clicking the button below:</p>
            <p style="text-align:center;">
              <a href="{verification_link}" 
                 style="display:inline-block;background-color:#FAAF5E;color:#fff;
                        padding:10px 16px;text-decoration:none;border-radius:6px;">
                Verify Email
              </a>
            </p>
            <p>If you didn’t request this, you can safely ignore this email.</p>
            <p>— The Momoy App Team</p>
          </body>
        </html>
        """

        # Send email
        # send_mail(
        #     subject="Verify your email",
        #     message=f"Click this link to verify your account: {verification_link}",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[email],
        #     fail_silently=False,  # will raise error if SMTP fails
        # )

        email_obj = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_obj.attach_alternative(html_message, "text/html")
        email_obj.send(fail_silently=False)

        return Response({"message": "Check your email to verify your account"}, status=status.HTTP_201_CREATED)
        

class VerifyEmailView(APIView):
    permission_classes = []
    
    def get(self, request):
        token = request.query_params.get("token")

        if not token:
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "email_verification_failed.html")
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pending = PendingEmailVerification.objects.get(token=token)
        except PendingEmailVerification.DoesNotExist:
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "email_verification_failed.html")
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=pending.email).exists():
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "email_verification_failed.html")
            return Response({"error": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=pending.email,
            email=pending.email,
            is_active=True
        )

        pending.delete()

        if "text/html" in request.META.get("HTTP_ACCEPT", ""):
            return render(request, "email_verification_success.html")

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
    

class UserAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = UserAddress.objects.filter(user=request.user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not UserAddress.objects.filter(user=request.user).exists():
            serializer.validated_data['is_default'] = True

        if serializer.validated_data.get('is_default', False):
            UserAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class UserAddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            address = UserAddress.objects.get(pk=pk, user=request.user)
        except UserAddress.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAddressSerializer(address, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # If updating to default, clear others
        if serializer.validated_data.get('is_default', False):
            UserAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            address = UserAddress.objects.get(pk=pk, user=request.user)
        except UserAddress.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response({"message": "Address deleted"}, status=status.HTTP_204_NO_CONTENT)


class SendLoginLinkView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"error": "No account found with this email"}, status=status.HTTP_404_NOT_FOUND)

        PendingLoginLink.objects.filter(created_at__lt=timezone.now() - datetime.timedelta(minutes=1)).delete()

        token = secrets.token_urlsafe(32)
        PendingLoginLink.objects.create(email=email, token=token)

        login_link = f"http://{request.get_host()}/auth/verify-login-link/?token={token}"

        subject = "You Have Received a Login Link"
        text_message = f"Click to log in instantly: {login_link}"
        html_message = f"""
        <html>
          <body style="font-family: Arial, sans-serif;">
            <h2>Welcome back to Momoy's App!</h2>
            <p>Click the button below to log in to your account:</p>
            <p style="text-align:center;">
              <a href="{login_link}" 
                 style="display:inline-block;background-color:#FAAF5E;color:#fff;
                        padding:10px 16px;text-decoration:none;border-radius:6px;">
                Log in to Momoy
              </a>
            </p>
            <p>This link expires in 1 minute.</p>
            <p>— The Momoy App Team</p>
          </body>
        </html>
        """
        try:
            email_obj = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_obj.attach_alternative(html_message, "text/html")
            email_obj.send(fail_silently=False)

            return Response({
                "message": "Login link sent! Check your email.",
                "expires_in": 60, 
                "expires_text": "1 minute"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error sending login link:", e)

            return Response(
                {"error": "Failed to send email", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyLoginLinkView(APIView):
    permission_classes = []

    def get(self, request):
        token = request.query_params.get("token")

        if not token:
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "login_link_failed.html")
            return Response({"error": "Missing token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pending = PendingLoginLink.objects.get(token=token)
        except PendingLoginLink.DoesNotExist:
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "login_link_failed.html")
            return Response({"error": "Invalid or expired link"}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - pending.created_at > datetime.timedelta(minutes=1):
            pending.delete()
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "login_link_failed.html")
            return Response({"error": "This link has expired"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=pending.email)
        except User.DoesNotExist:
            pending.delete()
            if "text/html" in request.META.get("HTTP_ACCEPT", ""):
                return render(request, "login_link_failed.html")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        pending.delete() 

        if "text/html" in request.META.get("HTTP_ACCEPT", ""):
            return render(request, "login_link_success.html")

        return Response({
            "message": "Login successful",
            "access": str(access),
            "refresh": str(refresh),
            "email": user.email,
        }, status=status.HTTP_200_OK)
