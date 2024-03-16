
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Collection
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.decorators import api_view
from .serializers import CollectionSerializer, CollectionListSerializer
from rest_framework.permissions import IsAuthenticated
from lingauth.models import CustomUser

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EditWordView(request):
    data = request.data
    collection_id = data.get('collection_id')
    title = data.get('title')
    collection = get_object_or_404(Collection, id=collection_id, owner=request.user)
    word_to_edit = next((word for word in collection.words if word['title'] == title), None)
    word_to_edit.update(data)
    collection.save()
    return Response({'message': 'Word updated successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RemoveWordView(request):
    data = request.data
    collection_id = data.get('collection_id')
    title = data.get('title')

    collection = get_object_or_404(Collection, id=collection_id, owner=request.user)
    # word = collection.words.filter(title=title).first()
    word_to_remove = None
    for word in collection.words:
        if word['title'] == title:
            word_to_remove = word
            break
    
    if word_to_remove:
        collection.words.remove(word_to_remove)
        collection.save()
        return Response({'message': 'Word removed successfully'})
    else:
        return Response({'message': 'Word not found in collection'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddWordView(request):
    data = request.data
    collection_id = data.get('collection_id')  # Include collection_id in your Axios request
    # collection = Collection.objects.get(id=collection_id, owner=request.user)
    collection = get_object_or_404(Collection, id=collection_id, owner=request.user)
    collection.words.append(data)
    collection.save()
    return Response({'message': 'Word added successfully'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemoveCollectionView(request, id):
    try:
        collection = Collection.objects.get(id=id, owner=request.user)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Collection.DoesNotExist:
        return Response({'error': 'Collection not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def CreateCollectionView(request):
    # serializer = CollectionSerializer(data=request.data, context={'owner': request.user})
    print("User:", request.user)  # Print user information to the console
    print("Request data:", request.data)  
    serializer = CollectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCollectionListView(ListAPIView):
    serializer_class = CollectionListSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust as needed

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        return Collection.objects.filter(owner=user)

class UserPublicListView(ListAPIView):
    serializer_class = CollectionListSerializer
    permission_classes = []  # Adjust as needed

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        return Collection.objects.filter(owner=user, isPublic=True)


class EditCollectionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer

    def post(self, request, id, *args, **kwargs):
        collection = get_object_or_404(Collection, id=id, owner=request.user)
        collection_settings = request.data 
        print(collection_settings)


        serializer = self.serializer_class(instance=collection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Collection edited successfully'})

    
    
class VisitCollectionView(APIView):
    authentication_classes = []  # Remove authentication classes
    permission_classes = []

    serializer_class = CollectionSerializer
    def get(self, request, id, *args, **kwargs):
        collection = get_object_or_404(Collection, id=id)
        serializer = self.serializer_class(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


