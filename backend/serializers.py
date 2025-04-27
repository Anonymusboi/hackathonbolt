from rest_framework import serializers
from .models import JobSeeker,Profile
from django.contrib.auth.models import User

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ('id','user', 'skills', 'experience', 'certifications', 'ready_to_work', 'anonymous_profile', 'success_story', 'resume')
        
class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'user_type', 'phone', 'address')
        
class CreateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user