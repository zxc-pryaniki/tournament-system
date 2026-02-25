from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginView(APIView):
    # access to unauth
    authentication_classes = [] 
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # if ok - 200
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        # 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)