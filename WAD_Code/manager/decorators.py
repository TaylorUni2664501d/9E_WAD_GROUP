from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse

def teamless_test_function(user):
    if user.is_a_captain or user.is_a_player:
        return False
    return True
    
    
def user_teamless(func):
    @wraps(func)
    def _wrapped_view(request, *args, **kwargs):
        if not teamless_test_function(request.user):
            messages.error(request, "You're already in a team!")
            return redirect("manager/view_team.html")
        return func(request, *args, **kwargs)
    return _wrapped_view
    