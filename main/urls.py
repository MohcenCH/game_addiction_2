from django.urls import path
from main.views import *
from dj_rest_auth.views import LogoutView
urlpatterns = [
    path("login/", CustomLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UserList.as_view(), name="users"),
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
]
