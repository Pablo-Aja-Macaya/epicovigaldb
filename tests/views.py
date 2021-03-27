import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import send_results_processing, update



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
          return render(request, 'tests/selection.html', {'message':'Tests corriendo!'})
        else:
          return render(request, 'tests/selection.html', {'warning':'Ningún test seleccionado.'})
        
@login_required(login_url="/accounts/login")
def send_results(request):
    import time
    # Apartado de subida de archivos de resultados
    def check_file(): # TO-DO
        pass   
    if request.method == 'POST':
        for file in request.FILES.getlist('documents'):
            start = time.time()
            send_results_processing(file)
            end = time.time()
            print('Tiempo para archivo:', end-start)
        return render(request, 'tests/upload_test_results.html', {'message':'Archivos subidos a la base de datos!'})

@login_required(login_url="/accounts/login")
def update_from_folder(request):
    print('Updating')
    print('='*50)
    unchanged, updated, new, errors = update()
    context = {'message':f'Actualización completa (Sin cambios: {unchanged}, Actualizados: {updated}, Nuevos: {new}, Errores: {errors})'}
    return render(request, 'tests/upload_test_results.html', context)