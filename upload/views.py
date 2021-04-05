from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
import io
import urllib.request

from .utils import upload_utils
from .tasks import find_coords


# Create your views here.
@login_required(login_url="/accounts/login")
def upload_manual(request):
    # tasks = Task.objects
    return render(request, 'upload/manual.html')

@login_required(login_url="/accounts/login")
def upload_csv(request):
    # tasks = Task.objects
    return render(request, 'upload/csv.html')

@login_required(login_url="/accounts/login")
def upload(request):
    def check_file(): # TO-DO
        pass     
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['document']
            data = uploaded_file.read().decode('UTF-8')
            io_string = io.StringIO(data)
            if request.POST.get('origin') == 'hospital':
                #upload_sample_hospital.delay(data)
                fallos, columnas_inesperadas = upload_utils.upload_sample_hospital(io_string)
                #find_coords.delay() # esto se hace por detrás con celery

                if fallos:
                    warning = f'<strong>Columnas inesperadas</strong>: {columnas_inesperadas}. <strong>Error en muestras:</strong> {fallos}, puede que tengan fechas incorrectas o algún fallo de formato. Completando nuevas coordenadas por detrás.'
                    messages.warning(request, warning)
                    # return render(request, 'upload/csv.html', {'warning':warning})
                else:
                    message = 'Se ha completado la actualización. Finalizando coordenadas por detrás.'
                    messages.success(request, message)
                    # return render(request, 'upload/csv.html', {'message':'Se ha completado la actualización. Finalizando coordenadas por detrás.'})      
                return redirect('csv')      
            else:
                message = 'Origen no implementado.'
                messages.warning(request, message)
                return redirect('csv')   
                # return render(request, 'upload/csv.html',{'warning':'Origen no implementado.'})
        except Exception as e:
            print(e)
            message='Algo ha ido mal (1).'
            messages.warning(request, message)
            return redirect('csv')   
            # return render(request, 'upload/csv.html',{'warning':'Algo ha ido mal (1).'})

    else:
        message = 'Algo ha ido mal (2).'
        messages.warning(request, message)
        return redirect('csv')   
        # return render(request, 'upload/csv.html',{'message':'Algo ha ido mal (2).'})
    


# Subida de metadatos directamente desde el GoogleSheet
@login_required(login_url="/accounts/login")
def update_from_google(request):
    from epicovigal.local_settings import GS_DATA_KEY as key
    from epicovigal.local_settings import GS_DATA_GID as gid
    
    enlace = f'https://docs.google.com/spreadsheets/d/{key}/export?format=tsv&gid={gid}'
    with urllib.request.urlopen(enlace) as google_sheet:
        data = google_sheet.read().decode('UTF-8')
        io_string = io.StringIO(data)
        fallos, columnas_inesperadas = upload_utils.upload_sample_hospital(io_string)
        #find_coords.delay() # esto se hace por detrás con celery        

    if fallos:
        warning = f'<strong>Columnas inesperadas</strong>: {columnas_inesperadas}. <strong>Error en muestras:</strong> {fallos}, puede que tengan fechas incorrectas o algún fallo de formato. Completando nuevas coordenadas por detrás.'
        messages.warning(request, warning)
        return redirect('csv') 
        # return render(request, 'upload/csv.html', {'warning':warning})
    else:
        message = 'Se ha completado la actualización desde GoogleSheets'
        messages.success(request, message)
        return redirect('csv') 
        # return render(request, 'upload/csv.html', {'message':message})


