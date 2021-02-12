import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import send_results_processing



# Create your views here.
@login_required(login_url="/accounts/login")
def tests(request):
    return render(request, 'tests/selection.html')

@login_required(login_url="/accounts/login")
def upload_test_results(request):
    return render(request, 'tests//upload_test_results.html')

@login_required(login_url="/accounts/login")
def send_selection(request):
    if request.method == 'POST':
        test_list = ['Picard','SingleCheck', 'NGSStats', 'NextClade', 'iVar', 'Lineages']
        selected_tests = {}
        print(request.POST)
        for i in test_list:
            if request.POST.get(i):
                selected_tests[i.lower()] = 1
            else:
                selected_tests[i.lower()] = 0
        print(selected_tests)
        # prueba() # celery

        if 1 in selected_tests.values():
          return render(request, 'tests/selection.html', {'message':'The tests are running!'})
        else:
          return render(request, 'tests/selection.html', {'warning':'No test selected'})
        
@login_required(login_url="/accounts/login")
def send_results(request):
    def check_file(): # TO-DO
        pass   
    if request.method == 'POST':
        for file in request.FILES.getlist('documents'):
            send_results_processing(file)
        return render(request, 'tests/upload_test_results.html', {'message':'On going'})
        
