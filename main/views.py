from dj_rest_auth.views import LoginView
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from.serializers import *
from .models import *
from django.http import Http404
from django.conf import settings
from dj_rest_auth.app_settings import (
    JWTSerializer, JWTSerializerWithExpiration, TokenSerializer,
)
from rest_framework import generics
from django.contrib.auth import authenticate, login
class CustomLogin(LoginView):
    def get_response(self):
        response = super().get_response()
        print("test")
        return response
    
    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            if getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False):
                response_serializer = JWTSerializerWithExpiration
            else:
                response_serializer = JWTSerializer

        else:
            response_serializer = TokenSerializer
        return response_serializer
    
class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def perform_create(self, serializer):
        user = serializer.save()
        user = authenticate(
            email=self.request.data.get("email"),
            password=self.request.data.get("password"),
        )
        if user and user.is_active:
            login(self.request, user)
class DoctorList(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

@api_view(['GET', 'POST'])
def questions(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT', 'DELETE'])
def questionDetail(request, id):
    try:
        question = Question.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        


@api_view(['GET', 'POST'])
def answers(request):
    if request.method == 'GET':
        answerOption = AnswerOption.objects.all()
        serializer = AnswerOptionSerializer(answerOption, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AnswerOptionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def answerDetail(request, id):
    try:
        question = Question.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        answer_options = question.answerOptions.all()
        serializer = AnswerOptionSerializer(answer_options, many = True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AnswerOptionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def questionResponses(request):
    if request.method == 'GET':
        questionResponse = QuestionResponse.objects.all()
        serializer = QuestionResponseSerializer(questionResponse, many=True)
        return Response(serializer.data)    
    elif request.method == 'POST':
        try:
            existing_entry = QuestionResponse.objects.filter(answer = request.data.get('answer'), questionnaire = request.data.get('questionnaire')).first()
            if existing_entry:
                serializer = QuestionResponseSerializer(existing_entry, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = QuestionResponseSerializer(data = request.data)
                if serializer.is_valid():       
                    serializer.save()
                    return Response(serializer.data, status = status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': 'IntegrityError'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def questionResponseDetail(request, id):
    try:
        questionResponse = QuestionResponse.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer = QuestionResponseSerializer(questionResponse)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = QuestionResponseSerializer(questionResponse, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def questionnaires(request):
    if request.method == 'GET':
        questionnaire = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaire, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionnaireSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

class PatientList(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

@api_view(['GET', 'PUT'])
def patientDetail(request, id):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  