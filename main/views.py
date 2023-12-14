from dj_rest_auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status   
from.serializers import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404


class CustomLogin(LoginView):
    def get_response(self):
        response = super().get_response()
        print("test")
        return response




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

@api_view(['GET','POST'])
def patients(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PatientSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


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

  