
from rest_framework import status, generics

from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework.views import APIView
from .models import CustomUser
from collection.models import Collection
from quiz.models import Quiz
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from .serializers import UserSerializerWithToken, MyTokenObtainPairSerializer, UserSerializer
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
    user = request.user

    if user.changedUsername and user.lastNicknameChange:
        if (user.lastNicknameChange + timedelta(days=14)) > timezone.now():
            time_remaining = (user.lastNicknameChange + timedelta(days=14)) - timezone.now()
            return Response({'error': f'{time_remaining.days} gün sonra değiştirilebilir'}, status=401)

    user_notifications = user.notifications or []
    notification = {
        'notification_emoji': '👀',
        'old_nickname': user.username,
        'item_id': 0,
        'type': 'nickname',
        'item_name': new_username,
        'date': str(timezone.now())
    }
    user_notifications.append(notification)
    user.notifications = user_notifications
  
    user.username = new_username
    user.lastNicknameChange = timezone.now()
    user.changedUsername = True

    user.save()


    return Response({'message': 'Username set successfully'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_data(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    quiz_data = request.data.get('quiz_data')
    
    if not quiz_data:
        return Response({"error": "No quiz_data provided"}, status=400)

    # Ensure user's quiz_data is a list
    if not isinstance(user.quiz_data, list):
        user.quiz_data = []

    try:
        print(f"Before appending: {len(user.quiz_data)}")
        user.quiz_data.append(quiz_data)
        user.save()
        print(f"After appending: {len(user.quiz_data)}")
        return Response(user.quiz_data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):

        user = request.user
        data = {
            'streak': user.streak,
            'locale': user.locale,
            'credits': user.credits,
            'activity': user.activity,
            'username': user.username,
            'quiz_data': user.quiz_data,
            'greenWall': user.greenWall,
            'saved_items': user.saved_items,
            'notifications': user.notifications,
            'studyProgress': user.studyProgress,
            'paymentMethods': user.paymentMethods,
            'lastRefillDate': user.lastRefillDate,
            'studyPreference': user.studyPreference,
            'lastPurchaseDate': user.lastPurchaseDate,
            'old_notifications': user.old_notifications,
            'current_week_data': user.current_week_data,
        }
        return Response(data)
    


    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_saved_data(request):
    item_data = request.data.get('item_data')

    if 'item_type' not in item_data or 'item_id' not in item_data:
        return Response({'error': 'Invalid item data'}, status=400)

    item_id = item_data['item_id']
    item_type = item_data['item_type']
    item_name = item_data['item_name']
    item_emoji = item_data['item_emoji']
    item_length = item_data['item_length']

    existing_saved_items = request.user.saved_items or []
    
    # Helper function to remove item from saved items
    def remove_saved_item(item_type, item_id):
        for saved_item in existing_saved_items:
            if saved_item['item_type'] == item_type and saved_item['item_id'] == item_id:
                existing_saved_items.remove(saved_item)
                request.user.saved_items = existing_saved_items
                request.user.save()
                return True
        return False

    # Helper function to update item star count
    def update_star_count(model, item_id):
        item = get_object_or_404(model, pk=item_id)
        existing_who_starred = item.whoStarred or []
        if request.user.id in existing_who_starred:
            existing_who_starred.remove(request.user.id)
            item.whoStarred = existing_who_starred
            item.save()
            return Response({'message': f'{item_type.capitalize()} removed from saved items'})
        else:
            existing_who_starred.append(request.user.id)
            item.whoStarred = existing_who_starred
            item.save()
            
            # Update item owner's notifications list
            owner = item.owner
            owner_notifications = owner.notifications or []
            notification = {
                'notification_emoji': '❤️',
                'who_favourited': request.user.username,
                'item_id': item_id,
                'type': item_type,
                'item_name': item_name,
                'date': str(timezone.now())
            }
            owner_notifications.append(notification)
            owner.notifications = owner_notifications
            owner.save()
            
            return Response({'message': 'Saved data updated successfully'})

    if item_type == 'collection':
        if remove_saved_item('collection', item_id):
            return update_star_count(Collection, item_id)
        else:
            existing_saved_items.append(item_data)
            request.user.saved_items = existing_saved_items
            request.user.save()
            return update_star_count(Collection, item_id)
    
    elif item_type == 'quiz':
        if remove_saved_item('quiz', item_id):
            return update_star_count(Quiz, item_id)
        else:
            existing_saved_items.append(item_data)
            request.user.saved_items = existing_saved_items
            request.user.save()
            return update_star_count(Quiz, item_id)
    
    return Response({'error': 'Invalid item type'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_read(request):
    try:
        user = request.user
        user_notifications = user.notifications or []

        # Move notifications to old_notifications
        user_old_notifications = user.old_notifications or []
        user_old_notifications.extend(user_notifications)
        user.old_notifications = user_old_notifications

        # Clear notifications
        user.notifications = []
        user.save()
        return Response({'message': 'Notifications marked as read successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_activity(request):
   
    try:
        user = request.user
        user_activity = user.activity or []

        # activity_data = request.data.get('activity_data')
        # activity_type = activity_data['activity_type']
        # activity_name = activity_data['activity_name']
        # activity_id = activity_data['activity_id']

        # Update current_week_data
     

        activity_type = request.data.get('activity_type')
        activity_name = request.data.get('activity_name')
        activity_id = request.data.get('activity_id')


         # Get today's date
        today_date = timezone.now().date()
        
        # Find the index of today's day (Monday = 0, Sunday = 6)
        today_index = today_date.weekday()

        # current_week_data = default_week_data.copy()
        # current_week_data = user.current_week_data or default_week_data.copy()
        current_week_data = user.current_week_data 

        # Update current_week_data based on today's date
        for i, day_data in enumerate(current_week_data):
    # Set isToday and user_activity if it's today
            if i == today_index:
                day_data['isToday'] = True
                day_data['user_activity'] = True
            else:
                # Reset isToday to False for other days
                day_data['isToday'] = False
                # Update hasPassed based on the comparison of their indexes with today's index
                day_data['hasPassed'] = i < today_index
                # Keep user_activity true if it's already set to true
                if day_data['user_activity']:
                    day_data['hasPassed'] = False


        if user_activity:
            # Get the date of the last activity
            last_activity_date = user_activity[-1].get('date')
            # Convert last_activity_date to a datetime object
            last_activity_date = datetime.strptime(last_activity_date, '%Y-%m-%d %H:%M:%S.%f%z').date()
            
            # If the last activity was yesterday, increment streak
            if last_activity_date == today_date - timedelta(days=1):
                # Increment the streak
                user.streak += 1
            # If the last activity was not yesterday, reset streak to 1
            elif last_activity_date < today_date - timedelta(days=1):
                user.streak = 1
            # If the last activity was today, do nothing to the streak
        else:
            # If there is no previous activity, start the streak from 1
            user.streak = 1
        
        activity = {
            'activity_type': activity_type,
            'activity_name': activity_name,
            'activity_id': activity_id,
            'username': user.id,
            'date': str(timezone.now())
        }

        user.streak = 1

        def get_day_of_year_today():
    # Get current date
            today = datetime.today()
            day_of_year = today.timetuple().tm_yday
            return day_of_year
        
        user.greenWall.append(get_day_of_year_today())
        print(user.greenWall)

        # user_activity.append(activity)
        user_activity = [activity]

        user.activity = user_activity
        # user.activity = []
        user.current_week_data = current_week_data
        user.save()

        return Response({'message': 'Activity listed successfuly'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    


class EditCollectionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        user_settings = request.data 
        print(user_settings)

        serializer = self.serializer_class(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User edited successfully'})

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