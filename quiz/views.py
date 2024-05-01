
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework.decorators import api_view
from .serializers import QuizSerializer
from rest_framework.permissions import IsAuthenticated
from lingauth.models import CustomUser

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def RemoveQuizView(request, id):
    try:
        collection = Quiz.objects.get(id=id, owner=request.user)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Quiz.DoesNotExist:
        return Response({'error': 'Quiz not found.'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def CreateQuizView(request):
    # serializer = QuizSerializer(data=request.data, context={'owner': request.user})
    print("User:", request.user)  # Print user information to the console
    print("Request data:", request.data)  

    # is_ai_made = request.data.get('isAImade', False)
    # request.data['isAImade'] = is_ai_made

    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VisitQuizView(APIView):
    authentication_classes = []  # Remove authentication classes
    permission_classes = []

    serializer_class = QuizSerializer
    def get(self, request, id, *args, **kwargs):
        collection = get_object_or_404(Quiz, id=id)
        serializer = self.serializer_class(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


