from typing import Any
from django.utils import timezone
from .models import User


class LogUserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
 
        if request.user.is_authenticated:
            user = request.user
            user.latest_activity = timezone.now()
            user.loginCount += 0.5
            user.save()
        

        return response
    
class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = request.user
            user.latest_activity = timezone.now()
            user.save()
        
        return response