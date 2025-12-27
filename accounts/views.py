from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class RegistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                "message":"User registered successfully",
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

