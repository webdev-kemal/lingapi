from .models import CustomUser
from .serializers import UserSerializerWithToken
from rest_framework_simplejwt.tokens import RefreshToken


def user_get_me(user: CustomUser):
    return {
        'user': UserSerializerWithToken(user).data,
        'refresh': str(RefreshToken.for_user(user)),
        'access': str(RefreshToken.for_user(user).access_token),
    }
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'me': user_get_me(user=user),
    }