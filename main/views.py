from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from dj_rest_auth.views import LoginView
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from.serializers import *
from .models import *
from django.http import Http404, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from dj_rest_auth.serializers import JWTSerializer, JWTSerializerWithExpiration, TokenSerializer
from rest_framework import generics
from django.contrib.auth import authenticate, login,update_session_auth_hash
from django.dispatch import Signal
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.password_validation import validate_password


loginSignal = Signal()
class CustomLogin(LoginView):
    def get_response(self):
        response = super().get_response()
        print("test")
        if self.request.user.is_authenticated:
            # Send the custom signal when the user logs in
            loginSignal.send(sender=self.request.user, custom_data='User logged in')

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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    def perform_create(self, serializer):
        user = serializer.save()
        user = authenticate(
            email=self.request.data.get("email"),
            password=self.request.data.get("password"),
        )
        if user and user.is_active:
            login(self.request, user)

class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        update_session_auth_hash(request, request.user)  

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    
@api_view(["GET", "PATCH", "DELETE"])
# @permission_classes([IsAuthenticated])
def userDetail(request, id):
    try:
        user = User.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PATCH":
        serializer = UserSerializer(user,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorList(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def surveys(request):
    if request.method == 'GET':
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SurveySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def surveyDetail(request, id):
    try:
        survey = Survey.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = SurveySerializer(survey)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        survey.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def questionDetail(request, id):
    try:
        question = Question.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = QuestionSerializer(question, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def questionnaires(request):
    if request.method == 'GET':
        questionnaires = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaires, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionnaireSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def questionnaires(request, id):
    try:
        questionnaire = Questionnaire.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = QuestionnaireSerializer(questionnaire)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = QuestionnaireSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class PatientList(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def patientDetail(request, id):
    try:
        patient = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        raise Http404("Patient does not exist")

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def questionTypes(request):
    if request.method == 'GET':
        questionTypes = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(questionTypes, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = QuestionTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def questionTypeDetail(request, id):
    try:
        questionType = QuestionType.objects.get(pk=id)
    except: 
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuestionTypeSerializer(questionType)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = PatientSerializer(questionType, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @permission_classes([IsAuthenticated])
# def messages_page(request):
#     threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
#     context = {
#         'Threads': threads
#     }
#     return render(request, 'messages.html', context)

@permission_classes([IsAuthenticated])
def usersGrowthRate(request):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    previousMonth = (datetime.now() - relativedelta(months = 1)).month
    previous2Month = (datetime.now()- relativedelta(months = 2)).month
    previous3Month = (datetime.now()- relativedelta(months = 3)).month
    if previousMonth == 12:
        previousCurrentYear = currentYear-1
    else:
        previousCurrentYear = currentYear

    if previous2Month == 12:
        previousCurrentYear2 = currentYear -1
    else:
        previousCurrentYear2 = currentYear

    if previous3Month == 12:
        previousCurrentYear3 = currentYear -1
    else:
        previousCurrentYear3 = currentYear
    previousMonthRegistrations = 0
    currentMonthRegisterations = 0


    currentMonthRegisterations = User.objects.filter(
        registration_date__isnull=False,
        registration_date__month = currentMonth,
        registration_date__year = currentYear
    ).count()

    if previousMonth == 12:
        previousCurrentYear = currentYear-1
    else:
        previousCurrentYear = currentYear

    previousMonthRegistrations = User.objects.filter(
        registration_date__isnull=False,
        registration_date__month = previousMonth,
        registration_date__year = previousCurrentYear
    ).count()

    previous2MonthRegistrations = User.objects.filter(
        registration_date__isnull=False,
        registration_date__month = previous2Month,
        registration_date__year = previousCurrentYear2
    ).count()

    previous3MonthRegistrations = User.objects.filter(
        registration_date__isnull=False,
        registration_date__month = previous3Month,
        registration_date__year = previousCurrentYear3
    ).count()

    
    if currentMonthRegisterations == 0:
        growthRate = 0
         
    elif previousMonthRegistrations == 0 or previousMonthRegistrations is None:
        growthRate = 100
        
    else:
        growthRate = ((currentMonthRegisterations - previousMonthRegistrations)/previousMonthRegistrations)*100
    
    return JsonResponse({
            'current_month_registrations':currentMonthRegisterations,
            'previous_month_registrations':previousMonthRegistrations,
            'nd_previous_month_registrations':previous2MonthRegistrations,
            'rd_previous_month_registrations':previous3MonthRegistrations,
            'growth_rate': growthRate,
            })
    
@permission_classes([IsAuthenticated])
def messagesGrowthRate(request):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    previousMonth = (datetime.now()- relativedelta(months = 1)).month
    previous2Month = (datetime.now()- relativedelta(months = 2)).month
    previous3Month = (datetime.now()- relativedelta(months = 3)).month
    if previousMonth == 12:
        previousCurrentYear = currentYear-1
    else:
        previousCurrentYear = currentYear

    if previous2Month == 12:
        previousCurrentYear2 = currentYear -1
    else:
        previousCurrentYear2 = currentYear

    if previous3Month == 12:
        previousCurrentYear3 = currentYear -1
    else:
        previousCurrentYear3 = currentYear

    currentMonthMessages = Message.objects.filter(
        date_of_sending__month = currentMonth,
        date_of_sending__year = currentYear
    ).count()

    previousMonthMessages = Message.objects.filter(
        date_of_sending__month = previousMonth,
        date_of_sending__year = previousCurrentYear
    ).count()

    previous2MonthMessages = Message.objects.filter(
        date_of_sending__month = previous2Month,
        date_of_sending__year = previousCurrentYear2
    ).count()

    previous3MonthMessages = Message.objects.filter(
        date_of_sending__month = previous3Month,
        date_of_sending__year = previousCurrentYear3
    ).count()

    if currentMonthMessages == 0:
        growthRate = 0
        
    elif previousMonthMessages == 0 or previousMonthMessages is None:
        growthRate = 100
        
    else:
        growthRate = ((currentMonthMessages - previousMonthMessages)/previousMonthMessages)*100
    
    return JsonResponse({
            'growth_rate': growthRate,
            'current_month_messages':currentMonthMessages,
            'previous_month_messages':previousMonthMessages,
            'nd_previous_month_messages':previous2MonthMessages,
            'rd_previous_month_messages':previous3MonthMessages,
            })
@permission_classes([IsAuthenticated])
def FeedbackRate(request):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    previousMonth = (datetime.now()- relativedelta(months = 1)).month
    previous2Month = (datetime.now()- relativedelta(months = 2)).month
    previous3Month = (datetime.now()- relativedelta(months = 3)).month
    if previousMonth == 12:
        previousCurrentYear = currentYear-1
    else:
        previousCurrentYear = currentYear

    if previous2Month == 12:
        previousCurrentYear2 = currentYear -1
    else:
        previousCurrentYear2 = currentYear

    if previous3Month == 12:
        previousCurrentYear3 = currentYear -1
    else:
        previousCurrentYear3 = currentYear

    currentMonthFeedbacks = Feedback.objects.filter(
        date__month = currentMonth,
        date__year = currentYear
    ).count()

    previousMonthFeedbacks = Feedback.objects.filter(
        date__month = previousMonth,
        date__year = previousCurrentYear
    ).count()

    previous2MonthFeedbacks = Feedback.objects.filter(
        date__month = previous2Month,
        date__year = previousCurrentYear2
    ).count()

    previous3MonthFeedbacks = Feedback.objects.filter(
        date__month = previous3Month,
        date__year = previousCurrentYear3
    ).count()

    if currentMonthFeedbacks == 0:
        growthRate = 0
        
    elif previousMonthFeedbacks == 0 or previousMonthFeedbacks is None:
        growthRate = 100
        
    else:
        growthRate = ((currentMonthFeedbacks - previousMonthFeedbacks)/previousMonthFeedbacks)*100
    
    return JsonResponse({
            'growth_rate': growthRate,
            'current_month_feedbacks':currentMonthFeedbacks,
            'previous_month_feedbacks':previousMonthFeedbacks,
            'nd_previous_month_feedbacks':previous2MonthFeedbacks,
            'rd_previous_month_feedbacks':previous3MonthFeedbacks,
            })

@permission_classes([IsAuthenticated])
def activeUsers(request):
    active_users = User.objects.all()
    active_user_ids = list(active_users.values_list('id', flat=True))

    return JsonResponse({'active_user_ids': active_user_ids, 'active_users_count': len(active_user_ids)})
@permission_classes([IsAuthenticated])
def usersType(request):
    patients = User.objects.filter(
        account_type = "Patient"
    ).count()
    doctors = User.objects.filter(
        account_type = "Doctor"
    ).count()
    admins = User.objects.filter(
        account_type = "Admin"
    ).count()

    return JsonResponse({
        "patients":patients,
        "doctors":doctors,
        "admins":admins,
        "total":admins+patients+doctors
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



@api_view(['GET'])
def userMessagesAPIView(request, msg_sender, msg_receiver):
    try:
        messages = Message.objects.filter(
            Q(sender=msg_sender, recipient=msg_receiver) | Q(sender=msg_receiver, recipient=msg_sender)
            )
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MessageSerializer(messages, many = True)
        return Response(serializer.data)

@api_view(['GET'])
def messagesList(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many = True)
        return Response(serializer.data)

class UserMessagesAPIViewf(APIView):
    def get(self, request, user_id):
        message_type = request.query_params.get('type')  # Get the 'type' query parameter from the request

        if message_type == 'sent':
            message = Message.objects.filter(sender=user_id)
        elif message_type == 'received':
            message = Message.objects.filter(recipient=user_id)
        else:
            return Response({'error': 'Invalid message type'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def createMessageAPIView(request):
    if request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'error': 'Invalid message'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteMessageAPIView(APIView):
    def delete(self, request, message_id):
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
  

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def feedbacksList(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FeedbackSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteFeedback(request, id):
    try:
        feedback = Feedback.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        feedback.delete()
        


@api_view(['GET'])  
def alertsList(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.account_type == 'Admin':
                alerts = Alert.objects.filter(
                    toUser = 'admin'
                )
                serializer = AlertSerializer(alerts, many = True)
                return Response(serializer.data)
            elif request.user.account_type == 'Doctor':
                alerts = Alert.objects.filter(
                    toUser = 'doctor'
                )
                serializer = AlertSerializer(alerts, many = True)
                return Response(serializer.data)
            else:
                return Response({"detail": "Permission denied"}, status=403)
            
@api_view(['PATCH','DELETE'])  
@permission_classes([IsAuthenticated])
def alertDetails(request, id):
    try:
        alert = Alert.objects.get(pk = id)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        alert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PATCH":
        serializer = AlertSerializer(alert,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





    