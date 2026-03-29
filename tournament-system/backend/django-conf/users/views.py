from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import LoginSerializer

class LoginView(APIView):
    authentication_classes = [] 
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        try:
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except AuthenticationFailed as e:
            return Response({"detail": str(e.detail)}, status=status.HTTP_401_UNAUTHORIZED)