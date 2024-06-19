from rest_framework import serializers
from .models import CustomUser  # Import your CustomUser model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'pfp', 'locale', 'username', 'changedUsername', 'credits', 'notifications', 'old_notifications', 'saved_items', 'is_premium', "activity", "streak", "current_week_data", "quiz_data"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
 
    def validate(self, attrs):
       data = super().validate(attrs)
       serializer = UserSerializerWithToken(self.user).data
     
    #    print(f"User data before adding to token payload: {serializer}")
       
       access_token_payload = AccessToken.for_user(self.user)
    #    print(f"Access token payload before adding custom claims: {access_token_payload}")
     
       for k, v in serializer.items():
           data[k] = v

       access_token_payload['email'] = self.user.email
    #    print(f"Access token payload after adding custom claims: {access_token_payload}")

       return data

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['token']

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        access_token_payload = AccessToken.for_user(obj)
        access_token = str(access_token_payload)

        # return {
        #     'user': {
        #         'email': obj.email,
        #         'id': obj.id,
    
        #     },
        #     'refresh': str(refresh),
        #     'access': access_token,
        # }

# class UserInfoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['credits', 'locale', 'username']

class QuizDataSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    quiz_id = serializers.CharField(max_length=100)
    choices_data = serializers.ListField(
        child=serializers.DictField()
    )