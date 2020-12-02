from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import prueba

# Create your views here.
@login_required(login_url="/accounts/login")
def tests(request):
    return render(request, 'tests/selection.html')

@login_required(login_url="/accounts/login")
def send_selection(request):
    if request.method == 'POST':
        test_list = ['Picard','SingleCheck', 'NGSStats', 'NextClade', 'iVar', 'Lineages']
        selected_tests = {}
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
        
 