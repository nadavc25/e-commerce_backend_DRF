# shop/views/auth_views.py
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer
from rest_framework import status, views
from rest_framework.response import Response
import firebase_admin
from firebase_admin import auth as firebase_auth

User = get_user_model()

class GoogleLoginAPIView(views.APIView):
    def post(self, request):
        id_token = request.data.get('id_token')
        print("Firebase token:", id_token)
        if not id_token:
            return Response({'error': 'Missing ID token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the ID token with Firebase Admin SDK
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            profile_picture = decoded_token.get('picture', '')

            # Retrieve or create the user in the database
            user, created = User.objects.update_or_create(
                firebase_uid=uid,
                defaults={
                    'username': email.split('@')[0],
                    'email': email,
                    'first_name': name.split(' ')[0] if name else '',
                    'last_name': name.split(' ')[1] if len(name.split(' ')) > 1 else '',
                    'profile_picture': profile_picture
                }
            )

            # Update additional fields if they are available
            if not created:
                user.username = email.split('@')[0]
                user.email = email
                user.first_name = name.split()[0] if name else user.first_name
                user.last_name = name.split()[-1] if name else user.last_name
                user.profile_picture = profile_picture
                user.save()

            # Generate token using the custom serializer
            token = MyTokenObtainPairSerializer.get_token(user)

            # Add custom data manually if necessary
            data = {
                'access': str(token.access_token),
                'refresh': str(RefreshToken.for_user(user)),
                'username': user.username,
                'email': user.email,
                'is_Admin': user.is_superuser,
                'Name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'profile_picture': user.profile_picture
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
