# accounts/views.py
import random
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import OTPSerializer, OTPVerifySerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SendOTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        # 4-digit ka random OTP generate karo
        otp = random.randint(1000, 9999)

        # Abhi ke liye, hum OTP ko console par print karenge
        # Real project mein yahaan SMS bhejne ka code aayega
        print(f"OTP for {phone_number} is: {otp}")

        # Session mein OTP save karo taaki verify kar sakein
        request.session['otp'] = otp
        request.session['phone_number'] = phone_number

        return Response({"success": "OTP sent successfully."}, status=status.HTTP_200_OK)


class VerifyOTPView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        otp = int(serializer.validated_data['otp']) # OTP ko integer mein badlo

        # Session se OTP nikalo
        session_otp = request.session.get('otp')
        session_phone = request.session.get('phone_number')

        if session_otp is None or session_phone != phone_number:
            return Response({"error": "First send OTP."}, status=status.HTTP_400_BAD_REQUEST)

        if otp != session_otp:
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # OTP a_chha hai, ab user ko find ya create karo
        # get_or_create: agar user milta hai toh use le aao, nahi toh naya bana do
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'username': phone_number} # username ko phone number hi set kar do
        )

        if created:
            print(f"New user created: {user.username}")
        else:
            print(f"User logged in: {user.username}")

        # User ke liye JWT tokens generate karo
        tokens = get_tokens_for_user(user)

        # Session a_chha kardo
        del request.session['otp']
        del request.session['phone_number']

        return Response(tokens, status=status.HTTP_200_OK)


class DeleteAccountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"success": "Account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)