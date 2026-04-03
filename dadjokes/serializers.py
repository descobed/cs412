from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    '''Takes in and serializes joke data'''
    class Meta:
        model = Joke
        fields = '__all__' # needs to be explicit they're saying
def create(self, validated_data):
    '''overrides superclass'''
    print(f'JokeSerializer.create, validated_data:={validated_data}')
    
    validated_data['joke'] = Joke.objects.first()
    return Joke.objects.create(**validated_data)


class PictureSerializer(serializers.ModelSerializer):
    '''Takes in and serializes picture data'''
    class Meta:
        model = Picture
        fields = '__all__' # needs to be explicit they're saying
def create(self, validated_data):
    '''overrides superclass'''
    print(f'PictureSerializer.create, validated_data:={validated_data}')
    
    validated_data['picture'] = Picture.objects.first()
    return Picture.objects.create(**validated_data)