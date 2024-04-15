# lingauth/urls.py

from django.urls import path, include
from .views import RemoveQuizView, CreateQuizView, VisitQuizView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('create/', CreateQuizView, name='create-quiz'),
    path('get/<str:id>/', VisitQuizView.as_view(), name='visit-quiz'),
    path('remove/<str:id>/', RemoveQuizView, name='remove-quiz'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
