from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model

from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken

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

            user, created = User.objects.get_or_create(
                username=email,
                defaults={"email": email, "first_name": first_name,
                    "last_name": last_name,}
            )

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
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": "Invalid token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
