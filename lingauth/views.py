
from rest_framework import status, generics

from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from .serializers import UserSerializerWithToken, MyTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from django.conf import settings
from urllib.parse import urlencode
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from .selectors import user_get_me

from .services import create_or_update_user_from_google_data, jwt_login
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework import permissions


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def UserInitApi(request):
    id_token = request.headers.get('Authorization')
    user = create_or_update_user_from_google_data(id_token=id_token)
    
    response_data = user_get_me(user=user)
    response = jwt_login(response=Response(data=response_data), user=user)

    return response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def registerUser(request):
    data = request.data
    try:
        user = CustomUser.objects.create(
            email=data['email'],
            password=make_password(data['password']),
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except Exception as e:
        message = {
            'details': str(e)
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializerWithToken(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_username(request):
    new_username = request.data.get('username')

    if not new_username:
        return Response({'error': 'Username is required'}, status=400)

    # Check if another user with the same username exists
    existing_user = CustomUser.objects.filter(username=new_username).exclude(id=request.user.id).first()
    if existing_user:
        return Response({'error': 'Username is already taken'}, status=400)

    # Set the new username and mark changedUsername as True
    request.user.username = new_username
    request.user.changedUsername = True
    request.user.save()

    return Response({'message': 'Username set successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_data(request):
    quizData = request.data.get('quiz_data')

    existing_quiz_data = request.user.quiz_data or []

    # Append the new quiz data to the existing data
    existing_quiz_data.append(quizData)

    # Update the user's quiz data field
    request.user.quiz_data = existing_quiz_data
    request.user.save()

    return Response({'message': 'Quiz data updated successfully'})

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'credits': user.credits,
            'locale': user.locale,
            'username': user.username,
            'quiz_data': user.quiz_data
        }
        return Response(data)

# def UserInitApi(request):
#     id_token = request.headers.get('Authorization')
#     google_user_data = google_validate_id_token(id_token=id_token)

#     user, created = user_get_or_create(email=google_user_data['email'])
    
#     response_data = user_get_me(user=user)
#     response = jwt_login(response=Response(data=response_data), user=user)

#     return response
      
# class LoginApi(ObtainJSONWebTokenView):
#     def post(self, request, *args, **kwargs):
#         # Reference: https://github.com/Styria-Digital/django-rest-framework-jwt/blob/master/src/rest_framework_jwt/views.py#L44
#         serializer = self.get_serializer(data=request.data)

#         serializer.is_valid(raise_exception=True)

#         user = serializer.object.get('user') or request.user
#         user_record_login(user=user)

#         return super().post(request, *args, **kwargs)
    

# class GoogleLoginApi(APIView):
#     class InputSerializer(serializers.Serializer):
#         code = serializers.CharField(required=False)
#         error = serializers.CharField(required=False)

#     def get(self, request, *args, **kwargs):
#         input_serializer = self.InputSerializer(data=request.GET)
#         input_serializer.is_valid(raise_exception=True)

#         validated_data = input_serializer.validated_data

#         code = validated_data.get('code')
#         error = validated_data.get('error')

#         login_url = f'{settings.BASE_FRONTEND_URL}/login'

#         if error or not code:
#             params = urlencode({'error': error})
#             return redirect(f'{login_url}?{params}')

#         domain = settings.BASE_BACKEND_URL
#         api_uri = reverse('api:v1:auth:login-with-google')
#         redirect_uri = f'{domain}{api_uri}'

#         access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

#         user_data = google_get_user_info(access_token=access_token)

#         profile_data = {
#             'email': user_data['email'],
#             'first_name': user_data.get('givenName', ''),
#             'last_name': user_data.get('familyName', ''),
#         }

#         # We use get-or-create logic here for the sake of the example.
#         # We don't have a sign-up flow.
#         user, _ = user_get_or_create(**profile_data)

#         response = redirect(settings.BASE_FRONTEND_URL)
#         response = jwt_login(response=response, user=user)

#         return response


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def set_username(request):
#     new_username = request.data.get('username')

#     if not new_username:
#         return Response({'error': 'Username is required'}, status=400)

#     request.user.username = new_username
#     request.user.changedUsername = True
#     request.user.save()

#     return Response({'message': 'Username set successfully'})


# class UserRegistrationView(APIView):
#     authentication_classes = []  # Exclude authentication for this view
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()

#             # Send email confirmation (optional)
#             # ...

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class RegistrationAPIView(generics.CreateAPIView):
#     serializer_class = CustomUserSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)

#         return Response(
#             {"access_token": access_token},
#             status=status.HTTP_201_CREATED
#         )