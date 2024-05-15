# django_app/firebase_middleware.py
from firebase_admin import auth as firebase_auth
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Extract the token from the "Bearer <token>" format
        token = auth_header.split(' ')[1] if len(auth_header.split(' ')) == 2 else None
        if not token:
            return None

        try:
            decoded_token = firebase_auth.verify_id_token(token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')

        # Retrieve or create a corresponding user in your Django database
        User = get_user_model()
        try:
            user = User.objects.get(firebase_uid=uid)
        except User.DoesNotExist:
            user = User.objects.create(
                firebase_uid=uid,
                username=email.split('@')[0],  # Using email prefix as username
                email=email
            )

        return (user, None)
