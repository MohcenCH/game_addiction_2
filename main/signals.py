from django.dispatch import receiver
from .models import *
from .views import loginSignal
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save


@receiver(loginSignal)
def loginSignalHandler(sender, custom_data, **kwargs):
    print("user has been logged in")

# @receiver(user_logged_in, sender = User)
# def updateLoginCount(sender, request, user, **kwargs):
#     user.loginCount += 1
#     user.save()

@receiver(post_save, sender = User)
def signup_alerts_handler(sender, instance, created, **args):
    if created:
        signUpAlert = Alert(
        fromUser = instance,
        content = f'New user registered: {instance.first_name} {instance.last_name}',
        toUser = "admin"
        )
        signUpAlert.save()

@receiver(post_save, sender = User)
def createSubUserHandler(sender, instance,created, **args):
    if created:
        if instance.account_type == 'Patient':
            subUser = Patient(
                user = instance
            )
            subUser.save()
            print("patient created")
        elif instance.account_type == 'Doctor':
            subUser = Doctor(
                user = instance
            )
            subUser.save()
            print("doctor created")



@receiver(post_save, sender = Survey)
def questionnaireAnswer(sender, instance, created, **args):
    if created:
        signUpAlert = Alert(
        fromUser = instance.patient.user,
        content = f'{instance.patient.user.first_name} {instance.patient.user.last_name} has answered the questionnaire',
        toUser = "doctor"
        )
        signUpAlert.save()


@receiver(post_save, sender = Feedback)
def feedbackNotification(sender, instance, created, **args):
    if created:
        signUpAlert = Alert(
        fromUser = instance,
        content = f'{instance.first_name} {instance.last_name} has sent a new feedback',
        toUser = "admin"
        )
        signUpAlert.save()
