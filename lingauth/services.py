from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.core.exceptions import ValidationError
from typing import Tuple
from .models import CustomUser  # Update import path
from django.utils import timezone

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

def validate_google_id_token(*, id_token: str) -> dict:
    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )

    # print("Google API response:", response.json())

    if not response.ok:
        raise ValidationError('id_token is invalid.')

    return response.json()

# def user_get_or_create(*, email: str) -> Tuple[CustomUser, bool]:
#     user, created = CustomUser.objects.get_or_create(email=email)

#     return user, created

def create_or_update_user_from_google_data(*, id_token: str) -> CustomUser:
    google_user_data = validate_google_id_token(id_token=id_token)

    email = google_user_data.get('email')
    pfp = google_user_data.get('picture')
    locale = google_user_data.get('locale')

    if not email:
        raise ValueError("Email not found in Google user data")

    user, created = CustomUser.objects.get_or_create(email=email)

    # Update user fields based on Google user data
    user.first_name = google_user_data.get('given_name', '')
    user.last_name = google_user_data.get('family_name', '')
    user.pfp = pfp
    user.locale = locale

    user.save()

    return user


def jwt_login(*, response: Response, user: CustomUser) -> Response:
    refresh = RefreshToken.for_user(user)
    access_token = RefreshToken.for_user(user).access_token

    # Set the token in the cookie
    response.set_cookie('your_custom_cookie_name', str(access_token), httponly=True)

    update_last_login(None, user)  # Update last login time
    return response
