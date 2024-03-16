# lingauth/urls.py

from django.urls import path
from .views import registerUser, UserInitApi, set_username, UserInfoView
from django.conf import settings
from django.conf.urls.static import static


# login_patterns = [
#     # path('', LoginApi.as_view(), name='login'),
#     path('google/', GoogleLoginApi.as_view(), name='login-with-google'),
# ]

urlpatterns = [
    # path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/', include(login_patterns)),
    path('register/', registerUser, name='user-register'),
    path('init/', UserInitApi, name='user-validate'),
    path('set-username/', set_username, name='set-username'),
    path('get/', UserInfoView.as_view(), name='get-userinfo'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.urls import path
# from .views import UserRegistrationView
# # from .views import RegistrationAPIView

# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='user-registration'),
#     #  path('register/', RegistrationAPIView.as_view(), name='register'),
#     # Add more URL patterns as needed
# ]