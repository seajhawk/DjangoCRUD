from rest_framework import serializers 
from . import models
 
 
class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shelter
        fields = ('name',
                  'location')

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dog
        fields = ('shelter',
                  'name',
                  'description',
                  'intake_date')

class ErrorSerializer(serializers.Serializer):
    error_message = serializers.CharField(max_length=200)
    
