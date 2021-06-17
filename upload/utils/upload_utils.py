import io, csv, itertools
from datetime import datetime
import dateutil.parser
from ..models import Region, Sample
from ..models import SampleMetaData
import re
import traceback
from geopy import Nominatim

# In[0]
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



def find_coords():
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
    return errores, actualizados, sin_coords


# In[1]
## FUNCIONES PRINCIPALES
def upload_sample_hospital(stream):
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
        'Vacunación (tipo)':'vacunacion_tipo',
        'Vacunación (dosis)':'vacunacion_dosis',
        'Vacunación (fecha última dosis)':'fecha_vacunacion_ultima_dosis',
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
    io_string = stream
    dialect = csv.Sniffer().sniff(io_string.readline())
    io_string.seek(0)
    fieldnames = io_string.readline().strip().split(str(dialect.delimiter))

    # Cambio de nombres de campos a los de la base de datos 
    lista_columnas_inesperadas = []
    for i in range(len(fieldnames)):
        if fieldnames[i] != '':
            try:
                fieldnames[i] = fields_correspondence[fieldnames[i]]
            except:
                print(f'Columna inesperada: {fieldnames[i]}')
                lista_columnas_inesperadas.append(fieldnames[i])
  
    reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect) 
    
    lista_fallos = []
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
            if not Region.objects.filter(cp=cp, localizacion=loc).exists():
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
            region_reference = Region.objects.get(cp=cp, localizacion=loc)
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
            
    return lista_fallos, lista_columnas_inesperadas


# def upload_sample_gisaid():
#     pass

# def upload_sample_transmit():
#     pass










    #         obj = Sample.objects.filter(id_uvigo=id_uvigo).first()
    #         region_reference = Region.objects.get(cp=cp, localizacion=loc)
    #         # Para actualizar
    #         if obj: 
    #             # Objeto para Sample
    #             obj.id_accession = None
    #             obj.id_region = region_reference
    #             obj.original_name = None
    #             obj.categoria_muestra = categoria_muestra
    #             obj.edad = edad
    #             obj.sexo = sexo
    #             obj.patient_status = hospitalizacion
    #             obj.nodo_secuenciacion = nodo_secuenciacion
    #             obj.fecha_muestra = f_muestra
    #             obj.observaciones = observaciones                     
    #             try:
    #                 obj.full_clean() # se comprueba si el objeto se ajusta a las reglas de su modelo
    #                 entradas_sample_para_actualizar.append(obj)
    #             except Exception as e:
    #                 print(e)
    #                 lista_fallos.append(id_uvigo)
                
    #             # Objeto para SampleMetaData
    #             obj = 0
    #             obj = SampleMetaData.objects.filter(id_uvigo=id_uvigo).first()
    #             obj.id_paciente = id_paciente
    #             obj.id_hospital = id_hospital
    #             obj.numero_envio = numero_envio
    #             obj.id_tubo = id_tubo
    #             obj.id_muestra = id_muestra
    #             obj.hospitalizacion = hospitalizacion
    #             obj.uci = uci
    #             obj.ct_orf1ab = orf1ab
    #             obj.ct_gen_e = gen_e
    #             obj.ct_gen_n = gen_n      
    #             obj.ct_rdrp = rdrp 
    #             obj.ct_s = ct_s 
    #             obj.fecha_envio_cdna = f_envio_cdna 
    #             obj.fecha_run_ngs = f_run_ngs 
    #             obj.fecha_entrada_fastq = f_entrada_fastq
    #             obj.fecha_sintomas = f_sintomas    
    #             obj.fecha_diagnostico = f_diagnostico     
    #             obj.fecha_entrada = f_entrada_uv                   
    #             try:
    #                 obj.full_clean() # se comprueba si el objeto se ajusta a las reglas de su modelo
    #                 entradas_samplemetadata_para_actualizar.append(obj)
    #             except Exception as e:
    #                 print(e)
    #                 lista_fallos.append(id_uvigo)                
    #         # Para crear
    #         else:
    #             obj = Sample(
    #                 id_uvigo = id_uvigo,
    #                 id_accession = None,
    #                 id_region = region_reference,
    #                 original_name = None,
    #                 categoria_muestra = categoria_muestra,
    #                 edad = edad,
    #                 sexo = sexo,
    #                 patient_status = hospitalizacion,
    #                 nodo_secuenciacion = nodo_secuenciacion,
    #                 fecha_muestra = f_muestra,
    #                 observaciones = observaciones                     
    #             )
    #             try:
    #                 obj.full_clean() # se comprueba si el objeto se ajusta a las reglas de su modelo
    #                 entradas_sample_para_crear.append(obj)
    #             except Exception as e:
    #                 #print(e)
    #                 lista_fallos.append(id_uvigo)

    #             obj = 0
    #             obj = SampleMetaData(
    #                 id_uvigo = Sample(id_uvigo=id_uvigo),
    #                 id_paciente = id_paciente,
    #                 id_hospital = id_hospital,
    #                 numero_envio = numero_envio,
    #                 id_tubo = id_tubo,
    #                 id_muestra = id_muestra,
    #                 hospitalizacion = hospitalizacion,
    #                 uci = uci,
    #                 ct_orf1ab = orf1ab,
    #                 ct_gen_e = gen_e,
    #                 ct_gen_n = gen_n,      
    #                 ct_rdrp = rdrp,
    #                 ct_s = ct_s, 
    #                 fecha_envio_cdna = f_envio_cdna,
    #                 fecha_run_ngs = f_run_ngs, 
    #                 fecha_entrada_fastq = f_entrada_fastq,
    #                 fecha_sintomas = f_sintomas,    
    #                 fecha_diagnostico = f_diagnostico,    
    #                 fecha_entrada = f_entrada_uv,                    
    #             )
    #             try:
    #                 obj.full_clean() # se comprueba si el objeto se ajusta a las reglas de su modelo
    #                 entradas_samplemetadata_para_crear.append(obj)
    #             except Exception as e:
    #                 #print(e)
    #                 lista_fallos.append(id_uvigo)


    #     except Exception as e:
    #         print(e)
    #         print(traceback.format_exc())
    #         lista_fallos.append(id_uvigo)

    # # BULK UPDATE
    # update_fields = [
    #     'id_accession',
    #     'id_region',
    #     'original_name',
    #     'categoria_muestra',
    #     'edad',
    #     'sexo',
    #     'patient_status',
    #     'nodo_secuenciacion',
    #     'fecha_muestra',
    #     'observaciones',
    # ]
    # Sample.objects.bulk_update(entradas_sample_para_actualizar, update_fields, batch_size=100)
    # update_fields = [
    #     'id_uvigo','id_paciente','id_hospital',
    #     'numero_envio','id_tubo','id_muestra',
        
    #     'hospitalizacion','uci',
        
    #     'ct_orf1ab','ct_gen_e','ct_gen_n','ct_rdrp','ct_s',

    #     'fecha_envio_cdna','fecha_run_ngs','fecha_entrada_fastq',
    #     'fecha_sintomas','fecha_diagnostico','fecha_entrada',

    # ]
    # SampleMetaData.objects.bulk_update(entradas_samplemetadata_para_actualizar, update_fields, batch_size=100)


    # # BULK CREATE
    # Sample.objects.bulk_create(entradas_sample_para_crear, batch_size=100)
    # Sample.objects.bulk_create(entradas_samplemetadata_para_crear, batch_size=100)