from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required

#@login_required(login_url="/accounts/login")
def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects
    else:
        tasks = Task.objects.filter(show_to='all')
    return render(request, 'tasks/home.html', {'tasks':tasks})







