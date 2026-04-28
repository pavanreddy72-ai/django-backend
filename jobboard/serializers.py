from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Job, Application

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'role', 'phone', 'company_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'phone', 'company_name', 'bio']

class JobSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.username', read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'employer', 'employer_name', 'title', 'company', 'location',
                  'job_type', 'description', 'requirements', 'salary', 'created_at', 'is_active']
        read_only_fields = ['employer', 'created_at']

class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'job_title', 'applicant', 'applicant_name',
                  'cover_letter', 'resume', 'status', 'applied_at']
        read_only_fields = ['applicant', 'applied_at']