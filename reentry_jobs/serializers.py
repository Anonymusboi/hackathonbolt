from rest_framework import serializers
from .models import JobSeeker

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ('id','user', 'skills', 'experience1', 'certifications', 'ready_to_work', 'anonymous_profile', 'success_story', 'resume')