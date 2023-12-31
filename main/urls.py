from django.urls import path
from main.views import *
from django.contrib.auth.views import PasswordChangeView
from dj_rest_auth.views import LogoutView
urlpatterns = [
    path("login/", CustomLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserList.as_view(), name="users"),
    path("users/<int:id>", userDetail),
    path("doctors/", DoctorList.as_view(), name="doctors"),
    path('questions/', questions),
    path('questions/<int:id>/', questionDetail),
    path('answer.options/', answers),
    path('answer.options/<int:id>/', answerDetail),
    path('question.responses/', questionResponses),
    path('question.responses/<int:id>/', questionResponseDetail),
    path('questionnaires/', questionnaires),
    path('patients/', PatientList.as_view(), name="patients"),
    path('patients/<int:id>/', patientDetail),
    path('surveys/',surveys ),
    path('surveys/<int:id>/',surveyDetail ),
    path('questions.types/',questionTypes ),
    path('questions.types/<int:id>/',questionTypeDetail ),
    path('statistics/users_growth_rate', usersGrowthRate),
    path('statistics/users_types/', usersType),
    path('statistics/messages_growth_rate/', messagesGrowthRate),
    path('statistics/feedbacks_growth_rate/', FeedbackRate),
    path('statistics/active_users/', activeUsers),
    path('statistics/current_user/', get_current_user),
    path('messages/<int:msg_sender>/<int:msg_receiver>', userMessagesAPIView),
    path('create-message/', createMessageAPIView),
    path('feedbacks/', feedbacksList),
    path('feedback_delete/<int:id>', deleteFeedback),
     path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('alerts/', alertsList,),
    path('alerts/<int:id>/', alertDetails),


]
