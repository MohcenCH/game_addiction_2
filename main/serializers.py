from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password as val_password


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__'

class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = '__all__'
class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["is_staff","is_superuser"]
        

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(UserSerializer, self).create(validated_data)
        return user
    
    def validate_password(self, value):
        val_password(value, self.instance)
        return value

class PatientSerializer(serializers.ModelSerializer):

    user = UserSerializer(required = False)
    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            patient = Patient.objects.create(user=user, **validated_data)
            return patient
        else:
            raise serializers.ValidationError(user_serializer.errors)
class DoctorSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'
        
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            doctor = Doctor.objects.create(user=user, **validated_data)
            return doctor
        else:
            raise serializers.ValidationError(user_serializer.errors)
        
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Message
        fields = '__all__'
        
class FeedbackSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Feedback
        fields = '__all__'