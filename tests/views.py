import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

from .models import send_results_processing, update, read_log
from .forms import *
from .test_execution import *

@login_required(login_url="/accounts/login")
def test_errors(request):
    error_log_file = './test_update_error_log.txt'
    errors = read_log(error_log_file)
    context = {'errors':errors}
    return render(request, 'tests/test_errors.html', context)

@login_required(login_url="/accounts/login")
def test_selection(request):
    if request.method=='POST':
        form = SelectTestForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            return redirect(reverse('input_selection', args=[datos['test']]))
    else:
        form = SelectTestForm()

    context = {
        'form':form,
        'url_form':reverse('test_selection'),
    }
    return render(request, 'tests/test_selection.html', context)

@login_required(login_url="/accounts/login")
def input_selection(request, test):
    form = ''
    cmd = ''
    if request.method=='POST':
        files = request.POST.getlist('files')
        _, cmd = find_test_data(test)
        execute_command(cmd, TESTS_OUTPUT_TMP)
        messages.success(request, 'Test estaría siendo ejecutado')
        return redirect(reverse('test_selection'))
    else:
        form = SelectInputForm() 
        choices, cmd = find_test_data(test)
        form.fields['files'].choices = ( (i,i) for i in choices)

    context = {
        'form':form,
        'url_form':reverse('input_selection', args=[test]),
        'command':cmd
    }
    return render(request, 'tests/input_selection.html', context)

@login_required(login_url="/accounts/login")
def upload_test_results(request):
    return render(request, 'tests/upload_test_results.html')


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