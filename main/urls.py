from django.urls import path
from main.views import *

urlpatterns = [
    path("login/", CustomLogin.as_view(), name="login"),
    path('questions/', questions),
    path('questions/<int:id>/', questionDetail),
    path('answer.options/', answers),
    path('answer.options/<int:id>/', answerDetail),
    path('question.responses/', questionResponses),
    path('question.responses/<int:id>/', questionResponseDetail),
    path('questionnaires/', questionnaires),
    path('patients/', patients),
    path('patients/<int:id>/', patientDetail)
]
