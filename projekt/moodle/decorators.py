from .models import Korisnici
from django.shortcuts import redirect


def mentor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_role == 'MENTOR':
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_role == 'STUDENT':
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap