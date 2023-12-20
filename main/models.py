from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from main.managers import UserManager
from django.contrib.auth import get_user_model
from django.db.models import Q


class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True,blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"

    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addiction_level = models.FloatField(max_length=255, null=True)
    average_hours_of_play_per_week = models.FloatField(null=True)
    average_months_of_play = models.FloatField(null=True)
    insomnia_score = models.FloatField(null=True)
    excessive_sleepiness_score = models.FloatField(null=True)
    anxiety_score = models.FloatField(null=True)
    depression_score = models.FloatField(null=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=255)
    planned_therapy_sessions = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Questionnaire(models.Model):
    name = models.CharField(max_length = 255)
    def __str__(self):
        return str(self.name)+" Questionnaire"

class QuestionType(models.Model):
    type = models.CharField(max_length = 255)
    def __str__(self):
        return self.type
class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete = models.CASCADE)
    text_of_question = models.TextField()
    question_type = models.ForeignKey(QuestionType, on_delete = models.DO_NOTHING)
    def __str__(self):
        return self.text_of_question

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answerOptions')
    answer_text = models.TextField()
    answer_point = models.FloatField()
    def __str__(self):
        return str(self.question.text_of_question)+" ==> "+str(self.answer_text)

class Survey(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.DO_NOTHING)
    questionnaire = models.ForeignKey(Questionnaire, on_delete = models.DO_NOTHING)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    def __str__(self):
        return str(self.questionnaire.name)+"; "+str(self.patient)
class QuestionResponse(models.Model):
    answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete = models.CASCADE)
    def __str__(self):
        self.survey = Survey.objects.select_related('questionnaire').get(pk=self.survey.pk)
        return str(self.survey)+', '+str(self.answer.answer_text)

    

# class QuestionnaireResponse(models.Model):
#     questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
#     question_response = models.ForeignKey(QuestionResponse, on_delete=models.CASCADE, null=True)


class Alert(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_alert = models.DateField()
    type_of_alert = models.CharField(max_length=255)


# class Message(models.Model):
#     thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
#     sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE)
#     message_content = models.TextField()
#     date_of_sending = models.DateTimeField()
#     def __str__(self):
#         return self.message_content


class UsageStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_statistic = models.DateField()


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)