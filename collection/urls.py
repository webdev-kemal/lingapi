# lingauth/urls.py

from django.urls import path, include
from .views import AddWordView, RemoveWordView, UserPublicListView, EditWordView, RemoveCollectionView, CreateCollectionView, UserCollectionListView, VisitCollectionView, EditCollectionView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/<str:username>/', UserCollectionListView.as_view(), name='user-collection-list'),
    path('public/<str:username>/', UserPublicListView.as_view(), name='user-public-collections'),
    path('create/', CreateCollectionView, name='create-collection'),
    path('get/<str:id>/', VisitCollectionView.as_view(), name='visit-collection'),
    path('edit/<str:id>/', EditCollectionView.as_view(), name='edit-collection'),
    path('remove/<str:id>/', RemoveCollectionView, name='remove-collection'),
    path('add-word/', AddWordView, name='add-word'),
    path('remove-word/', RemoveWordView, name='remove-word'),
    path('edit-word/', EditWordView, name='edit-word'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
