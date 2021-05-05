from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
import io
import re
import urllib.request

from .utils import upload_utils
from .tasks import find_coords
from .forms import FullSampleForm
from django.urls import reverse
from .models import *
from .utils.upload_utils import clean_location, find_sample_name


# Create your views here.
@login_required(login_url="/accounts/login")
def upload_manual(request):
    # tasks = Task.objects
    if request.method=='POST':
        form = FullSampleForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            sample_name = find_sample_name(datos.get('id_uvigo'))
            if sample_name:
                region_fields = ['cp','localizacion','pais','region','latitud','longitud']
                defaults_region = {i:datos.get(i) for i in region_fields}
                defaults_region['localizacion'] = clean_location(defaults_region['localizacion'])

                sample_fields = [
                    'id_uvigo','id_accession','id_region','original_name',
                    'categoria_muestra','edad','sexo','patient_status','nodo_secuenciacion',
                    'fecha_muestra','observaciones'
                ]
                defaults_sample = {i:datos.get(i) for i in sample_fields}

                samplemetadata_fields = [
                    'id_uvigo','id_paciente','id_hospital','numero_envio',
                    'id_tubo','id_muestra','hospitalizacion','uci',
                    'ct_orf1ab','ct_gen_e','ct_gen_n','ct_rdrp','ct_s',
                    'fecha_sintomas','fecha_diagnostico','fecha_entrada',
                    'fecha_envio_cdna','fecha_run_ngs','fecha_entrada_fastq'                
                ]
                defaults_samplemetadata = {i:datos.get(i) for i in samplemetadata_fields}

                try:
                    _, created = Region.objects.update_or_create(
                            cp = datos.get('cp'),
                            localizacion = datos.get('localizacion'),
                            defaults = defaults_region

                        )
                    region_reference = Region.objects.get(cp=datos.get('cp'), localizacion=datos.get('localizacion'))
                    defaults_sample['id_region'] = region_reference
                    _, created = Sample.objects.update_or_create(
                            id_uvigo = datos.get('id_uvigo'),
                            defaults = defaults_sample

                        )
                    sample_reference = Sample.objects.get(id_uvigo=datos.get('id_uvigo'))
                    defaults_samplemetadata['id_uvigo'] = sample_reference
                    _, created = SampleMetaData.objects.update_or_create(
                            id_uvigo = sample_reference,
                            defaults = defaults_samplemetadata

                        )
                    enlace_muestra = reverse('specific_sample', args=(datos.get('id_uvigo'),))
                    enlace = f'<a href="{enlace_muestra}">{datos.get("id_uvigo")}</a>'
                    messages.success(request, f'Cambios guardados. Perfil de muestra: {enlace}')
                    return redirect(reverse('manual'))                        
                except Exception as e:
                    messages.warning(request, f'Error en alguno de los datos ({e})')
                    return redirect(reverse('manual')) 

            else:
                messages.warning(request, 'Error en nombre de muestra')
                return redirect(reverse('manual'))                
    else:
        form = FullSampleForm()

    context = {
        'form':form,
        'url_form':reverse('manual')
    }
    return render(request, 'upload/manual.html', context)

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

@login_required(login_url="/accounts/login") 
def update_coords(request):
    errores, actualizados, sin_coords = find_coords()
    u = 'https://epicovigaldb.com/visualize/regions?sort=latitud'
    message = f'Coordenadas actualizadas: {errores} errores, {actualizados} actualizados. Quedan {sin_coords} <a href={u}>regiones sin coordenadas</a>.'
    messages.success(request, message)
    return redirect('csv') 

# Subida de metadatos directamente desde el GoogleSheet
@login_required(login_url="/accounts/login")
def update_from_google(request):
    from epicovigal.local_settings import GS_DATA_KEY as key
    # from epicovigal.local_settings import GS_DATA_GID as gid
    from epicovigal.local_settings import GS_DATA_GID_LIST as gid_list    
    
    fallos_totales = []
    columnas_inesperadas_totales = []
    for gid in gid_list:
        enlace = f'https://docs.google.com/spreadsheets/d/{key}/export?format=tsv&gid={gid}'
        with urllib.request.urlopen(enlace) as google_sheet:
            data = google_sheet.read().decode('UTF-8')
            io_string = io.StringIO(data)
            fallos, columnas_inesperadas = upload_utils.upload_sample_hospital(io_string)
            fallos_totales += fallos
            columnas_inesperadas_totales += columnas_inesperadas
            #find_coords.delay() # esto se hace por detrás con celery        

    if fallos_totales and columnas_inesperadas_totales:
        warning = f'<strong>Columnas inesperadas</strong>: {columnas_inesperadas_totales}. <strong>Error en muestras:</strong> {fallos_totales}, puede que tengan fechas incorrectas o algún fallo de formato.'
        messages.warning(request, warning)
        return redirect('csv') 
    elif fallos_totales:
        warning = f'<strong>Error en muestras:</strong> {fallos_totales}, puede que tengan fechas incorrectas o algún fallo de formato.'
        messages.warning(request, warning)
        return redirect('csv')         
    elif fallos_totales:
        warning = f'<strong>Columnas inesperadas</strong>: {columnas_inesperadas_totales}'
        messages.warning(request, warning)
        return redirect('csv')    
    else:
        message = 'Se ha completado la actualización desde GoogleSheets'
        messages.success(request, message)
        return redirect('csv') 


