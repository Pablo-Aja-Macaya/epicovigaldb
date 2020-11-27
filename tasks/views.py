from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login")
def home(request):
    tasks = Task.objects
    return render(request, 'tasks/home.html', {'tasks':tasks})







