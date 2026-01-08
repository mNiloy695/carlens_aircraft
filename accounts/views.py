from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer,LoginSerializer,UserAccountActivationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from random import randint
from .tasks import send_otp_email_task
from .models import OTP
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            code = randint(100000,999999)
            OTP.objects.create(user=user, code=code, type='registration')
            message = f"Hello {user.full_name}\n\n Your verification code is: {code} ! It will expire in 10 minutes.\n\nThank you for registering with us!\n\nBest regards,\nMultiAI Platform Team"
            send_otp_email_task.delay(subject="Welcome to MultiAI Platform 🚀",user_email=user.email,message=message,message_type='registration')
        
#             send_otp_email_task.apply_async(
#     args=(),  # if you have only kwargs, leave empty
#     kwargs={
#         "subject": "Welcome to MultiAI Platform 🚀",
#         "user_email": user.email,
#         "message": message,
#         "message_type": "registration"
#     }
# )

            return Response({"message": "User registered successfully. Please check your email for the verification code."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccountView(APIView):
    def post(self, request):
        serializer = UserAccountActivationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_active = True
            user.save()
            
            OTP.objects.filter(user=user, type='registration').delete()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            refresh=RefreshToken.for_user(user)
            return Response({
                "message":"Login successful",
                "user":{
                    "email":user.email,
                    "full_name":user.full_name,
                    "phone":user.phone,
                    "date_joined":user.date_joined,
                    "is_active":user.is_active,
                    "is_staff":user.is_staff,
                },
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self,request):
        try:
            refresh_token=request.data["refresh"]
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                "message":"Logout successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error":"Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)
        

from .serializers import ForgotPasswordSerializer
from django.shortcuts import get_object_or_404

class ForgotPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "No account found with this email."},
                    status=status.HTTP_404_NOT_FOUND
                )

            code = randint(100000, 999999)
            OTP.objects.create(user=user, code=code, type='registration')
            
            message = f"Hello! Your temporary code is {code}. It will expire in 10 minutes."
            send_otp_email_task.delay(
                subject="Forgot Password 🚀",
                user_email=email,
                message=message,
                message_type='forgot password'
            )
            return Response({"success": "OTP sent successfully to your email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .serializers import ResetPasswordSerializer

class ResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not available on this email"}, status=status.HTTP_404_NOT_FOUND)

            otp = OTP.objects.filter(user=user, code=code).first()
            if not otp:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            if otp.is_expired():
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
            
            # Delete OTP after successful use
            otp.delete()

            return Response({"success": "Password reset successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)