from rest_framework import serializers
from .models import Quiz  # Import your CustomUser model

class QuizSerializer(serializers.ModelSerializer):

    quiz_owner_username = serializers.SerializerMethodField(read_only=True)
    quiz_owner_pfp = serializers.SerializerMethodField(read_only=True)
    # owner_quiz_count = serializers.SerializerMethodField(read_only=True)
    # collections = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'
        read_only_fields = ['owner']

    def get_quiz_owner_username(self, obj):
        return obj.owner.username if obj.owner else None    

    def get_quiz_owner_pfp(self, obj):
        return obj.owner.pfp if obj.owner else None    
    
    # def get_owner_quiz_count(self, obj):
    #     return obj.owner.get_quiz_count() if obj.owner else None