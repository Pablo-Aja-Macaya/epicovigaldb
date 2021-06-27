from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.urls.base import reverse_lazy

from .subida_tests import send_results_processing, update, read_log
from .forms import *
from .test_execution import *
import os
import pathlib


STATUS_URL = reverse_lazy('check_status')


@login_required(login_url="/accounts/login")
def test_errors(request):
    error_log_file = './test_update_error_log.txt'
    errors = read_log(error_log_file)
    context = {'errors':errors}
    return render(request, 'tests/test_errors.html', context)

@login_required(login_url="/accounts/login")
def executed_tests_results(request, file=None):
    if file:
        with open(f'{TESTS_OUTPUT}/{file}','rt') as archivo:
            lines = archivo.readlines()
            lines= [l.replace('\t', ';') for l in lines]
            lines= [l.replace(';', ' ; ') for l in lines]
        context = {'lines':lines}
    else:
        # Archivos y fechas de modificación
        files = glob.glob(f'{TESTS_OUTPUT}/*')
        mtimes = [pathlib.Path(f).stat().st_mtime for f in files]
        
        # Obtener únicamente nombre de archivo y fecha formateada
        files = [os.path.basename(f) for f in files]
        mtimes = [datetime.fromtimestamp(t).strftime('%Y-%m-%d-%H:%M') for t in mtimes]

        info = list(zip(files, mtimes))
        info = sorted(info, key=lambda x: x[1], reverse=True) 
        context = {'files':info}

    return render(request, 'tests/test_results.html', context)

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
    cmd_function_dicc = CMD_FUNCTION_DICT
    if request.method=='POST':
        files = request.POST.getlist('files')
        _, cmd_function = find_test_data(test)
        execute_command.delay(files, cmd_function, TESTS_OUTPUT_TMP)
        messages.success(request, f'Tests se están ejecutando. <a href={STATUS_URL}>Comprueba el status de la tarea.</a>')
        return redirect(reverse('test_selection'))
    else:
        form = SelectInputForm() 
        choices, cmd_function = find_test_data(test)
        cmd_function = cmd_function_dicc[cmd_function]
        cmd = cmd_function('archivo')
        form.fields['files'].choices = ((i,i) for i in choices)

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
    # unchanged, updated, new, errors = update()
    update.delay()
    messages.success(request, f'Actualizando. <a href={STATUS_URL}>Comprueba el status de la tarea.</a>')
    return redirect('upload_test_results')

