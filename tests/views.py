import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

from .models import send_results_processing, update
from .forms import SelectTestForm



@login_required(login_url="/accounts/login")
def tests(request):
    if request.method=='POST':
        form = SelectTestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            datos = form.cleaned_data
            messages.success(request, 'Cambios guardados')
            return redirect(reverse('selection'))
    else:
        form = SelectTestForm()

    context = {
        'form':form,
        'url_form':reverse('selection'),
    }
    return render(request, 'tests/selection.html', context)

@login_required(login_url="/accounts/login")
def upload_test_results(request):
    return render(request, 'tests/upload_test_results.html')

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
        errors = []
        for file in request.FILES.getlist('documents'):
            try:
                send_results_processing(file)
            except:
                print(f'Error en {file.name}')
                errors.append(file.name)

        if errors:
            # context = {'warning':f'Problema: {len(errors)} archivo(s) {tuple(errors)} contienen problemas y no se han subido.'}
            messages.warning(request, f'Problema: {len(errors)} archivo(s) {tuple(errors)} contienen problemas y no se han subido.')
        else:
            # context = {'message':'Archivos subidos a la base de datos!'}
            messages.success(request, 'Archivos subidos a la base de datos!')
        
        # request.session['context'] = context
        return redirect('upload_test_results')
        # return render(request, 'tests/upload_test_results.html', context)

@login_required(login_url="/accounts/login")
def update_from_folder(request):
    unchanged, updated, new, errors = update()
    messages.success(request, f'Actualización completa (Sin cambios: {unchanged}, Actualizados: {updated}, Nuevos: {new}, Errores: {errors})')
    return redirect('upload_test_results')

    # context = {'message':f'Actualización completa (Sin cambios: {unchanged}, Actualizados: {updated}, Nuevos: {new}, Errores: {errors})'}
    # request.session['context'] = context
    # return render(request, 'tests/upload_test_results.html', context)