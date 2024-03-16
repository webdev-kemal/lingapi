from rest_framework import serializers
from .models import Collection  # Import your CustomUser model

class CollectionSerializer(serializers.ModelSerializer):

    owner_username = serializers.SerializerMethodField(read_only=True)
    owner_pfp = serializers.SerializerMethodField(read_only=True)
    owner_collection_count = serializers.SerializerMethodField(read_only=True)
    # collections = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['owner']

    def get_owner_username(self, obj):
        return obj.owner.username if obj.owner else None    

    def get_owner_pfp(self, obj):
        return obj.owner.pfp if obj.owner else None    
    
    def get_owner_collection_count(self, obj):
        return obj.owner.get_collection_count() if obj.owner else None
    
    # def get_collections(self, obj):
    #     collections = Collection.objects.filter(owner=obj.owner)
    #     serializer = CollectionSerializer(instance=collections, many=True, context=self.context)
    #     return serializer.data

    # def get_collections(self, obj):
    #     collections = Collection.objects.filter(owner=obj.owner)
    #     serializer = CollectionSerializer(collections, many=True)
    #     return serializer.data

class CollectionListSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField(read_only=True)
    owner_pfp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'

    def get_owner_username(self, obj):
        return obj.owner.username

    def get_owner_pfp(self, obj):
        return obj.owner.pfp if obj.owner else None    
