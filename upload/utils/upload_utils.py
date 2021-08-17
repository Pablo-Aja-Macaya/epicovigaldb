import io, csv, itertools
import dateutil.parser
from ..models import Region, Sample
from ..models import SampleMetaData
import re
import traceback
from geopy import Nominatim

from epicovigal.celery import app
from datetime import datetime
import urllib.request


# In[0]
## FUNCIONES DE STATUS
from jobstatus.models import start_process, finish_process, failed_process
from jobstatus.models import Status


# In[1]
## FUNCIONES AYUDANTES
def clean_location(loc):
    repl = str.maketrans("ÁÉÍÓÚ","AEIOU") # para quitar acentos
    # Quitar acentos y cosas raras a localización
    loc = loc.upper().translate(repl)
    # Algunas son 'CORUÑA (A)', lo siguiente se usa para transformarlas en A CORUÑA
    if '(O)' in loc:
        loc = 'O ' + loc[:-4]
    elif '(A)' in loc:
        loc = 'A ' + loc[:-4]
    
    return loc

def check_numbers(number):
    try:
        float(number)
        return number
    except:
        return None

def find_sample_name(string):
    # Encontrar si una cadena contiene alguna de las siguientes cosas:
        # Posibilidades:  EPI.X.N , SERGAS.X.N y VAL.X.N
    formats = [r'EPI\.\D+\.\d+.\.', r'SERGAS\.\D+\.\d+.\.', r'VAL\.\D+\.\d+.\.']
    accept = False
    # Probar las posibilidades, si encaja alguna se devuelve el nombre obtenido
    for i in formats:
        sample_name = re.search(i,string.replace('_','.')+'.')
        if sample_name:
            return sample_name.group()[:-1]
    # Si ninguna encaja se devuelve None
    return None

def time_transform(date):
    # Esta función comprueba que sea una fecha y pasa de dia/mes/año a año/mes/dia para la base de datos
    # Funciona tanto si el año es xx como xxxx
    try:
        transformed = dateutil.parser.parse(date, dayfirst=True,).strftime('%Y-%m-%d')
        if len(transformed) != 10: 
            # algunas fechas si están mal resultan en '202-12-23' (9 caracteres), inválido para SQL
            # Obligando a que sean de 10 caracteres se soluciona esto
            transformed = None
    except:
        transformed = None
    return transformed


def coords(place):
    geolocator = Nominatim(user_agent='test')
    try:
        location = geolocator.geocode(place)
        return location.latitude,location.longitude
    except:
        return None,None

def full_place_info(place):
    geolocator = Nominatim(user_agent='test')
    location = geolocator.geocode(place, addressdetails=True)
    try:
        raw_loc = location.raw['address']
        return location.latitude, location.longitude, raw_loc['state'], raw_loc['country']
    except: 
        return None, None, None, None


@app.task(bind=True)
def find_coords(self):
    start = datetime.now()
    id = self.request.id
    command = 'Actualizar_Coordenadas'
    start_process(id, command, start.strftime('%Y-%m-%d %H:%M:%S'))
    print(f'Starting coords update... (Task ID: {id})')

    try:
        data = Region.objects.filter(longitud=None) |  Region.objects.filter(longitud='NULL') | Region.objects.filter(longitud='0')
        sin_coords = len(data)
        # print('Lugares sin coordenadas:',sin_coords)
        errores = 0
        actualizados = 0
        for obj in data:
            lat = obj.latitud
            long = obj.longitud

            country = obj.pais
            loc = obj.localizacion
            cp = obj.cp

            if len(loc)>2:
                lat, long = coords(str(cp)+' '+ loc + ' ' + country)
                obj.latitud = lat
                obj.longitud = long
                obj.save()
                if lat is None:
                    # print(f'Could not update: {cp}, {loc}')
                    errores += 1   
                else:
                    # print(f'Updated: {cp}, {loc}, {lat}, {long}')
                    actualizados += 1
            else:
                obj.latitud = None
                obj.longitud = None
                obj.save()
                # print(f'No cumple condición: {cp}, {loc}')
                errores += 1                 
    
        # print('Finished updating coordinates')
        sin_coords -= actualizados

        finish = datetime.now()
        elapsed_time = finish - start
        mensaje = f'Coordenadas actualizadas: {errores} errores, {actualizados} actualizados.'
        finish_process(id, elapsed_time.seconds, mensaje)

        # return errores, actualizados, sin_coords
    except Exception as e:
        finish = datetime.now()
        elapsed_time = finish - start
        failed_process(id, elapsed_time.seconds, e)



# In[2]
## FUNCIONES PRINCIPALES
@app.task(bind=True)
def upload_sample_hospital(self):
    from epicovigal.local_settings import GS_DATA_KEY as key
    # from epicovigal.local_settings import GS_DATA_GID as gid
    from epicovigal.local_settings import GS_DATA_GID_LIST as gid_list

    start = datetime.now()
    id = self.request.id
    command = 'GS_Hospitales'
    start_process(id, command, start.strftime('%Y-%m-%d %H:%M:%S'))
    print(f'Starting hospital sample upload... (Task ID: {id})')

    fallos_totales = []
    columnas_inesperadas_totales = []
    fields_correspondence = {
        'Código UVIGO':'id_uvigo',
        'Categoría muestra':'categoria_muestra',
        'Vigilancia':'vigilancia',
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
        'Calidad secuenciación':'calidad_secuenciacion',
        'Vacunación tipo':'vacunacion_tipo',
        'Vacunación dosis':'vacunacion_dosis',
        'Vacunación fecha última dosis':'fecha_vacunacion_ultima_dosis',
        'QC VAF':'qc_vaf',
        'QC numero de mutaciones':'qc_numero_mutaciones',
        'Ct ORF1ab':'ct_orf1ab', 
        'Ct gen E':'ct_gen_e', 
        'Ct gen N':'ct_gen_n', 
        'Ct RdRP':'ct_rdrp', 
        'Ct S':'ct_s', 
        'Hospitalización paciente (S/N)':'hospitalizacion', 
        'UCI paciente (S/N)':'uci', 
        'Entrada muestra UVIGO':'fecha_entrada',
        'Fecha inicio síntomas (DD/MM/AAAA)':'fecha_sintomas', 
        'Fecha diagnóstico (DD/MM/AAAA)':'fecha_diagnostico', 
        'Fecha envío cDNA':'fecha_envio_cdna', 
        'Nodo de secuenciación':'nodo_secuenciacion', 
        'Fecha run NGS':'fecha_run_ngs', 
        'Entrada FASTQ UVIGO':'fecha_entrada_fastq', 
        'Observaciones':'observaciones',
    }
    lista_fallos = []
    lista_columnas_inesperadas = []
    for gid in gid_list:
        enlace = f'https://docs.google.com/spreadsheets/d/{key}/export?format=tsv&gid={gid}'
        with urllib.request.urlopen(enlace) as google_sheet:
            data = google_sheet.read().decode('UTF-8')
            io_string = io.StringIO(data)

        dialect = csv.Sniffer().sniff(io_string.readline())
        io_string.seek(0)
        fieldnames = io_string.readline().strip().split(str(dialect.delimiter))

        # Cambio de nombres de campos a los de la base de datos 
        for i in range(len(fieldnames)):
            if fieldnames[i] != '':
                try:
                    fieldnames[i] = fields_correspondence[fieldnames[i]]
                except:
                    print(f'Columna inesperada: {fieldnames[i]}')
                    lista_columnas_inesperadas.append(fieldnames[i])
    
        reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect) 
         
        for line in reader:
            try:
                id_uvigo = line.get('id_uvigo')
                id_hospital = line.get('id_hospital')
                id_paciente = str(line.get('id_paciente'))
                numero_envio = line.get('numero_envio')
                id_tubo = line.get('id_tubo')
                id_muestra = line.get('id_muestra')
                hospitalizacion = line.get('hospitalizacion')[:1] # Para que si hay un 'Si' pille sólo la S
                uci = line.get('uci')
                qc_vaf = line.get('qc_vaf')
                qc_numero_mutaciones = line.get('qc_numero_mutaciones')
                vacunacion_tipo = line.get('vacunacion_tipo')
                vacunacion_dosis = line.get('vacunacion_dosis')
                calidad_secuenciacion = line.get('calidad_secuenciacion')
                categoria_muestra = line.get('categoria_muestra')
                vigilancia = line.get('vigilancia')
                nodo_secuenciacion = line.get('nodo_secuenciacion')
                observaciones = line.get('observaciones')
                cp = line.get('cp')
                loc_org = line.get('localizacion')
                sexo = line.get('sexo','')[:1].upper()
                edad = line.get('edad')
                
                # Formateo de los ct (cambiar coma por puntos y cambiar espacio en blanco por 0 (quizás mejor Null?)) 
                orf1ab = line.get('ct_orf1ab').replace(',','.')
                gen_e = line.get('ct_gen_e').replace(',','.')
                gen_n = line.get('ct_gen_n').replace(',','.')
                rdrp = line.get('ct_rdrp').replace(',','.')
                ct_s = line.get('ct_s').replace(',','.')

                orf1ab = check_numbers(orf1ab)
                gen_e = check_numbers(gen_e)
                gen_n = check_numbers(gen_n)
                rdrp = check_numbers(rdrp)
                ct_s = check_numbers(ct_s)       

                try: 
                    int(cp)
                except: cp = 0

                try:
                    int(vacunacion_dosis)
                except:
                    vacunacion_dosis=None
                    
                try:
                    int(edad)
                except: edad = None

                # Formateo de fechas
                f_muestra = time_transform(line.get('fecha_muestra'))
                f_sintomas = time_transform(line.get('fecha_sintomas'))
                f_diagnostico = time_transform(line.get('fecha_diagnostico'))
                f_entrada_uv = time_transform(line.get('fecha_entrada'))
                f_envio_cdna = time_transform(line.get('fecha_envio_cdna'))
                f_run_ngs = time_transform(line.get('fecha_run_ngs'))
                f_entrada_fastq = time_transform(line.get('fecha_entrada_fastq'))
                f_vacunacion_ultima_dosis = time_transform(line.get('fecha_vacunacion_ultima_dosis'))

                loc = clean_location(loc_org)
                # latitud, longitud, division, pais = full_place_info(f'{cp} {loc_org}')

                if id_hospital=='ICVS':
                    pais = 'Portugal'
                    division = 'Portugal'
                else:
                    pais = 'España'
                    division = 'Galicia'

                # Insertado en la base de datos
                if not Region.objects.filter(cp=cp, localizacion=loc, localizacion_org__contains=loc_org).exists():
                    _, created = Region.objects.update_or_create(
                            cp = int(cp),
                            localizacion = loc,
                            defaults={
                                'cp' : int(cp),
                                'localizacion' : loc,
                                'localizacion_org' : loc_org,
                                'division' : division,
                                'pais' : pais,
                                'region' : 'Europa'
                            }
                        )
                region_reference = Region.objects.get(cp=cp, localizacion=loc, localizacion_org__contains=loc_org)
                if id_uvigo:
                    _, created = Sample.objects.update_or_create(
                            id_uvigo = id_uvigo,
                            defaults = {
                                'id_uvigo' : id_uvigo,
                                'id_accession' : None,
                                'id_region' : region_reference,
                                'original_name' : None,
                                'categoria_muestra':categoria_muestra,
                                'vigilancia':vigilancia,
                                'edad' : edad,
                                'sexo' : sexo[:1].upper(),
                                'patient_status' : hospitalizacion,
                                'nodo_secuenciacion' : nodo_secuenciacion,
                                'fecha_muestra' : f_muestra,
                                'observaciones' : observaciones                        
                            }

                        )
                    sample_reference = Sample.objects.get(id_uvigo=id_uvigo)
                    _, created = SampleMetaData.objects.update_or_create(
                            id_uvigo = sample_reference,
                            defaults = {
                                'id_uvigo' : sample_reference,
                                'id_paciente' : id_paciente,
                                'id_hospital' : id_hospital,
                                'numero_envio' : numero_envio,
                                'id_tubo' : id_tubo,
                                'id_muestra' : id_muestra,
                                'hospitalizacion' : hospitalizacion[:1], 
                                'uci' : uci[:1],
                                'qc_vaf':qc_vaf,
                                'qc_numero_mutaciones':qc_numero_mutaciones,
                                'vacunacion_tipo':vacunacion_tipo,
                                'vacunacion_dosis':vacunacion_dosis,
                                'ct_orf1ab' : orf1ab,
                                'ct_gen_e' : gen_e,
                                'ct_gen_n' : gen_n,
                                'ct_rdrp' : rdrp,
                                'ct_s' : ct_s,
                                'calidad_secuenciacion':calidad_secuenciacion,
                                'fecha_sintomas' : f_sintomas,
                                'fecha_diagnostico' : f_diagnostico,
                                'fecha_entrada' : f_entrada_uv,
                                'fecha_envio_cdna' : f_envio_cdna,
                                'fecha_run_ngs' : f_run_ngs,
                                'fecha_entrada_fastq' : f_entrada_fastq,
                                'fecha_vacunacion_ultima_dosis':f_vacunacion_ultima_dosis                   
                            }

                        ) 
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                lista_fallos.append(id_uvigo)

    finish = datetime.now()
    elapsed_time = finish - start
    if lista_fallos and lista_columnas_inesperadas:
        mensaje = f'Problema: {lista_fallos}. No procesadas: {lista_columnas_inesperadas}'
    elif lista_fallos:
        mensaje = f'Problema: {lista_fallos}'
    elif lista_columnas_inesperadas:
        mensaje = f'No procesadas: {lista_columnas_inesperadas}'
    else:
        mensaje = 'Actualizado desde google sheet'
    finish_process(id, elapsed_time.seconds, mensaje)
    

@app.task(bind=True)
def upload_prueba(self):
    start = datetime.now()
    id = self.request.id
    command = 'GS_Hospitales'
    
    start_process(id, command, start.strftime('%Y-%m-%d %H:%M:%S'))
    
    print(f'Starting hospital sample upload... (Task ID: {id})')
    print(2)
    try:
        # Procesar
        # ---------
        # Terminar proceso
        print(0)
        finish = datetime.now()
        elapsed_time = finish - start
        finish_process(id, elapsed_time.seconds, 'esto es un comentario success')
        print(f'Sample upload finished! (Elapsed time (s): {elapsed_time.seconds} (Task ID: {id})')
    except:
        finish = datetime.now()
        print(1)
        elapsed_time = finish - start
        print(f'Sample upload failed! (Elapsed time (s): {elapsed_time.seconds} (Task ID: {id})')
        failed_process(id, elapsed_time.seconds, 'esto es un comentario de un fallido')

