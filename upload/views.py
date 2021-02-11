from django.shortcuts import render
from .tasks import find_coords
from django.contrib.auth.decorators import login_required

# Función de upload
import io, csv
from datetime import datetime
import dateutil.parser
from .models import Region, Sample, SampleMetaData
from .utils import upload_utils



def upload_sample_hospital(stream):
    fields_correspondence = {
        'Código UVIGO':'id_uvigo', 
        'Entrada muestra UVIGO':'fecha_entrada_uv', 
        'Hospital extracción':'id_hospital', 
        'Nº Envío':'numero_envio', 
        'ID tubo':'id_tubo', 
        'ID muestra':'id_muestra', 
        'Fecha toma muestra (DD/MM/AAAA)':'fecha_muestra', 
        'ID paciente':'id_paciente', 
        'Sexo paciente (H/M)':'sexo', 
        'Edad paciente (años)':'edad', 
        'Ciudad residencia paciente':'localizacion', 
        'Código postal residencia paciente':'cp', 
        'Ct ORF1ab':'ct_orf1ab', 
        'Ct gen E':'ct_gen_e', 
        'Ct gen N':'ct_gen_n', 
        'Ct RdRP':'ct_rdrp', 
        'Ct S':'ct_s', 
        'Hospitalización paciente (S/N)':'hospitalizacion', 
        'UCI paciente (S/N)':'uci', 
        'Fecha inicio síntomas (DD/MM/AAAA)':'fecha_sintomas', 
        'Fecha diagnóstico (DD/MM/AAAA)':'fecha_diagnostico', 
        'Fecha envío cDNA':'fecha_envio_cdna', 
        'Nodo de secuenciación':'nodo_secuenciacion', 
        'Fecha run NGS':'fecha_run_ngs', 
        'Entrada FASTQ UVIGO':'fecha_entrada_fastq_uvigo', 
        'Observaciones':'observaciones',
    }
    def time_transform(date):
        # Esta función comprueba que sea una fecha y pasa de dia/mes/año a año/mes/dia para la base de datos
        # Funciona tanto si el año es xx como xxxx
        try:
            transformed = dateutil.parser.parse(date, dayfirst=True,).strftime('%Y-%m-%d')
        except:
            transformed = None
        return transformed
    
    # substitute = 'id_uvigo;fecha_entrada_uv;id_hospital;numero_envio;id_tube;id_sample;collection_date;
    # id_patient;gender;age;location;cp;ct_orf1ab;ct_gen_e;ct_gen_n;ct_rdrp;hospitalizacion;uci;fecha_sintomas;
    # fecha_diagnostico;observaciones'

    io_string = stream
    dialect = csv.Sniffer().sniff(io_string.readline())
    io_string.seek(0)
    fieldnames = io_string.readline().strip().split(str(dialect.delimiter))[:-1] ### CUIDADO CON ESTE [:-1] se pone para eliminar un elemento que se crea al haber un ; al final de la cabecera (columna en blanco)

    # Cambio de nombres de campos a los de la base de datos 
    for i in range(len(fieldnames)):
        fieldnames[i] = fields_correspondence[fieldnames[i]]
  
    reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect) 
    
    repl = str.maketrans("ÁÉÍÓÚ","AEIOU") # para quitar acentos
    
    for line in reader:
        id_linea = line['id_uvigo']
        id_hospital = line['id_hospital']
        id_patient = str(line['id_paciente'])
        envio = line['numero_envio']
        tube = line['id_tubo']
        id_sample = line['id_muestra']
        hosp = line['hospitalizacion'][:1]
        uci = line['uci']
        nodo = line['nodo_secuenciacion']
        comentarios = line['observaciones']
        postal_code = line['cp']
        loc = line['localizacion']
        sex = line['sexo']
        age = line['edad']
        
        # Formateo de los ct (cambiar coma por puntos y cambiar espacio en blanco por 0 (quizás mejor Null?)) 
        orf1ab = line['ct_orf1ab'].replace(',','.')
        gen_e = line['ct_gen_e'].replace(',','.')
        gen_n = line['ct_gen_n'].replace(',','.')
        rdrp = line['ct_rdrp'].replace(',','.')
        ct_s = line['ct_s'].replace(',','.')

        def check_numbers(number):
            try:
                float(number)
                return number
            except:
                return None

        orf1ab = check_numbers(orf1ab)
        gen_e = check_numbers(gen_e)
        gen_n = check_numbers(gen_n)
        rdrp = check_numbers(rdrp)
        ct_s = check_numbers(ct_s)       

        try: 
            int(postal_code)
        except: postal_code = 0
            
        try:
            int(age)
        except: age = 0

        # Formateo de fechas
        f_muestra = time_transform(line['fecha_muestra'])
        f_sintomas = time_transform(line['fecha_sintomas'])
        f_diagnostico = time_transform(line['fecha_diagnostico'])
        f_entrada_uv = time_transform(line['fecha_entrada_uv'])
        f_envio_cdna = time_transform(line['fecha_envio_cdna'])
        f_run_ngs = time_transform(line['fecha_run_ngs'])
        f_entrada_fastq_uvigo = time_transform(line['fecha_entrada_fastq_uvigo'])

        # Quitar acentos y cosas raras a localización
        loc = loc.upper().translate(repl)
        # Algunas son 'CORUÑA (A)', lo siguiente se usa para transformarlas en A CORUÑA
        if '(O)' in loc:
            loc = 'O ' + loc[:-4]
        elif '(A)' in loc:
            loc = 'A ' + loc[:-4]

        # Insertado en la base de datos
        if not Region.objects.filter(cp=postal_code, localizacion=loc).exists():
            _, created = Region.objects.update_or_create(
                    cp = int(postal_code),
                    localizacion = loc,
                    pais = 'SPAIN',
                    region = 'EUROPE',
                    latitud = 0,
                    longitud = 0
                )
            
        if not Sample.objects.filter(id_uvigo=id_linea).exists():
            _, created = Sample.objects.update_or_create(
                    id_uvigo = id_linea,
                    id_accession = 'NULL',
                    id_region = Region.objects.get(cp=postal_code, localizacion=loc).pk,
                    original_name = 'NULL',
                    edad = age,
                    sexo = sex[:1].upper(),
                    patient_status = hosp,
                    nodo_secuenciacion = nodo,
                    fecha_muestra = f_muestra,
                    observaciones = comentarios
                )
            
        if not SampleMetaData.objects.filter(id_uvigo=id_linea).exists():
            _, created = SampleMetaData.objects.update_or_create(
                    id_uvigo = id_linea,
                    id_paciente = id_patient,
                    id_hospital = id_hospital,
                    numero_envio = envio,
                    id_tubo = tube,
                    id_muestra = id_sample,
                    hospitalizacion = hosp[:1], 
                    uci = uci[:1],
                    ct_orf1ab = orf1ab,
                    ct_gen_e = gen_e,
                    ct_gen_n = gen_n,
                    ct_redrp = rdrp,
                    ct_s = ct_s,
                    fecha_sintomas = f_sintomas,
                    fecha_diagnostico = f_diagnostico,
                    fecha_entrada_uv = f_entrada_uv,
                    fecha_envio_cdna = f_envio_cdna,
                    fecha_run_ngs = f_run_ngs,
                    fecha_entrada_fastq_uvigo = f_entrada_fastq_uvigo
                ) 


# Create your views here.
@login_required(login_url="/accounts/login")
def upload_manual(request):
    # tasks = Task.objects
    return render(request, 'upload/manual.html')#, {'tasks':tasks})

@login_required(login_url="/accounts/login")
def upload_csv(request):
    # tasks = Task.objects
    return render(request, 'upload/csv.html')#, {'tasks':tasks})

@login_required(login_url="/accounts/login")
def upload(request):
    def check_file(): # TO-DO
        pass     
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        data = uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data)
        if request.POST.get('origin') == 'hospital':
            #upload_sample_hospital.delay(data)
            upload_sample_hospital(io_string)
            #find_coords.delay() # esto se hace por detrás con celery
            return render(request, 'upload/csv.html', {'message':'Finishing in the back!'})
        # try:
            # uploaded_file = request.FILES['document']
            # data = uploaded_file.read().decode('UTF-8')
            # io_string = io.StringIO(data)
            # if request.POST.get('origin') == 'hospital':
            #     #upload_sample_hospital.delay(data)
            #     upload_sample_hospital(io_string)
            #     return render(request, 'upload/csv.html', {'message':'Uploading in the back!'})
            
        #     else:
        #         return render(request, 'upload/csv.html',{'warning':'Origin not implemented yet'})
        # except Exception as e:
        #     print(e)
        #     return render(request, 'upload/csv.html',{'warning':'Something went wrong (1).'})

    else:
        return render(request, 'upload/csv.html',{'message':'Something went wrong (2).'})
    





# @login_required(login_url="/accounts/login")
# def upload(request):
#     import csv, io
#     from datetime import datetime
    
#     ##############################
#     def coords(place):
#         from geopy import Nominatim
#         # import time
#         geolocator = Nominatim(user_agent='test')
#         # time.sleep(1) 
#         try:
#             location = geolocator.geocode(place)
#             return location.latitude,location.longitude
#         except:
#             return 'NULL','NULL'
    
#     def check_file():
#         pass
    
#     ###############################
#     def upload_sample_hospital(io_string):
#         substitute = 'id_uvigo;fecha_entrada_uv;id_hospital;numero_envio;id_tube;id_sample;collection_date;id_patient;gender;age;location;cp;ct_orf1ab;ct_gen_e;ct_gen_n;ct_rdrp;hospitalizacion;uci;fecha_sintomas;fecha_diagnostico;observaciones'
#         fieldnames = substitute.split(';')
#         dialect = csv.Sniffer().sniff(io_string.readline())
#         # io_string.seek(0)      
#         reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect) 
        
#         repl = str.maketrans("ÁÉÍÓÚ","AEIOU") # para quitar acentos
#         for line in reader:
#             codigo = line['cp']
#             loc = line['location']
#             id_linea = line['id_uvigo']
#             age = line['age']
#             patient = str(line['id_patient'])
#             orf1ab = line['ct_orf1ab'].replace(',','.')
#             gen_e = line['ct_gen_e'].replace(',','.')
#             gen_n = line['ct_gen_n'].replace(',','.')
#             rdrp = line['ct_rdrp'].replace(',','.')
            
#             if orf1ab == '': orf1ab = 0.00
#             if gen_e == '': gen_e = 0.00
#             if gen_n == '': gen_n = 0.00
#             if rdrp == '': rdrp = 0.00
            
#             try: 
#                 collection_d = datetime.strptime(line['collection_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
#             except: pass
#             try: 
#                 f_sintomas = datetime.strptime(line['fecha_sintomas'], '%d/%m/%Y').strftime('%Y-%m-%d')
#             except: pass
#             try: 
#                 f_diagnostico = datetime.strptime(line['fecha_diagnostico'], '%d/%m/%Y').strftime('%Y-%m-%d')
#             except: pass
#             try: 
#                 f_entrada_uv = datetime.strptime(line['fecha_entrada_uv'], '%d/%m/%Y').strftime('%Y-%m-%d')            
#             except: pass
        
#             try: 
#                 int(codigo)
#             except: codigo = 0
            
#             try:
#                 int(age)
#             except: age = 0
            
#             if not Region.objects.filter(cp=codigo, location=loc).exists():
#                 lat, long = coords(str(codigo)+' '+ loc + ' ' + 'SPAIN')
#                 _, created = Region.objects.update_or_create(
#                     cp = int(codigo),
#                     location = loc.upper().translate(repl),
#                     latitude = lat,
#                     longitude = long
#                 )
            
#             if not Sample.objects.filter(id_uvigo=id_linea).exists():
#                 _, created = Sample.objects.update_or_create(
#                     id_uvigo = id_linea,
#                     id_accession = 'NULL',
#                     id_region = Region.objects.get(cp=codigo, location=loc.upper().translate(repl)).pk,
#                     original_name = 'NULL',
#                     age = age,
#                     gender = line['gender'][:1].upper(),
#                     patient_status = line['hospitalizacion'],
#                     originating_lab = 'UVIGO',
#                     collection_date = collection_d,
#                     additional_info = line['observaciones']
#                 )
            
#             if not SampleMetaData.objects.filter(id_uvigo=id_linea).exists():
#                 _, created = SampleMetaData.objects.update_or_create(
#                     id_uvigo = id_linea,
#                     id_patient = patient,
#                     numero_envio = line['numero_envio'],
#                     id_tube = line['id_tube'],
#                     id_sample = line['id_sample'],
#                     hospitalizacion = line['hospitalizacion'][:1], 
#                     uci = line['uci'][:1],
#                     ct_orf1ab = orf1ab,
#                     ct_gen_e = gen_e,
#                     ct_gen_n = gen_n,
#                     ct_redrp = rdrp,
#                     fecha_sintomas = f_sintomas,
#                     fecha_diagnostico = f_diagnostico,
#                     fecha_entrada_uv = f_entrada_uv
#                 )         

#     def upload_sample_gisaid():
#         pass

#     def upload_sample_transmit():
#         pass
    
#     ###############################       
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         data = uploaded_file.read().decode('UTF-8')
#         io_string = io.StringIO(data)
#         if request.POST.get('origin') == 'hospital':
#             upload_sample_hospital(io_string)
#             return render(request, 'upload/csv.html', {'message':'Upload completed succesfully!'})
        
#         else:
#             return render(request, 'upload/csv.html',{'warning':'Origin not implemented yet'})

#     else:
#         return render(request, 'upload/csv.html',{'message':'Something went wrong.'})
    