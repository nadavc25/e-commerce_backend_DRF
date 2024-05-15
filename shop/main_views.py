# main_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
from shop.models import User
from shop.views.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["get"])
def index(request):
    return Response("hello")

class Logout(APIView):
    def post(self, request):
        try:
            # Retrieve refresh token from the request
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                # Blacklist the token
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"error": "Missing refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def register(request):
    print(request)
    # Get username and password from the request data
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user if the username is unique
    user = User.objects.create_user(username=username, password=password, email=email)

    # You can customize the response according to your needs
    return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
