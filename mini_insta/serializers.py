from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    """Takes in a user and serialize it"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        '''overrides superclass'''
        print(f'UserSerializer.create, validated_data:={validated_data}')
        return User.objects.create_user(**validated_data)

class TodoSerializer(serializers.ModelSerializer):
    """Takes in a todo and serialize it"""
    class Meta:
        model = Todo
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    """Takes in a profile and serialize it"""
    class Meta:
        model = Profile
        fields = '__all__'
    
    def create(self, validated_data):
        '''overrides superclass'''
        print(f'ProfileSerializer.create, validated_data:={validated_data}')
        return Profile.objects.create(**validated_data)  

class PostSerializer(serializers.ModelSerializer):
    """Takes in a post and serialize it"""
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        """overrides superclass"""  
        print(f'PostSerializer.create, validated_data:={validated_data}')
        validated_data['profile'] = Profile.objects.first()
        return Post.objects.create(**validated_data)


class PhotoSerializer(serializers.ModelSerializer):
    """Serialize the photo model"""
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data):
        """overrides superclass"""
        print(f'PhotoSerializer.create, validated_data:={validated_data}')
        return Photo.objects.create(**validated_data)

#comments
#likes
#follows
