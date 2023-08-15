from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

@database_sync_to_async
def get_user(token_key):
    try:
        print("we are here body")
        jwt_authentication = JWTAuthentication()
        user, _ = jwt_authentication.authenticate(AccessToken(token_key))

        print(f"this is get user function token {user}")
        return user
    except:
        return AnonymousUser()

@database_sync_to_async    
def get_user_by_token(token):
    try:
        # Validate the token
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        # Handle token validation errors
        return None

    # Get the user ID from the token payload
    user_id = UntypedToken(token).get('user_id')

    # Get the User model
    User = get_user_model()

    try:
        # Get the user associated with the user ID
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return AnonymousUser()
    

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'Token' or token_name == 'Bearer':
                scope['user'] = await get_user_by_token(token_key)
        return await super().__call__(scope, receive, send)
