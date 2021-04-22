# -*- coding: utf-8 -*-
from epicovigal.celery import app
from upload.models import Region, Sample
from upload.models import SampleMetaData 
from jobstatus.models import Status
import io, csv
from datetime import datetime

@app.task
def upload_csv_task(number):
    print('Uploading file...', number)





def coords(place):
    from geopy import Nominatim
    # import time
    geolocator = Nominatim(user_agent='test')
    # time.sleep(1) 
    try:
        location = geolocator.geocode(place)
        return location.latitude,location.longitude
    except:
        return None,None

@app.task
def find_coords():
    data = Region.objects.filter(longitud=None) |  Region.objects.filter(longitud='NULL')
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
            print(f'Updated {cp}, {loc}, {lat}, {long}')   
        else:
            obj.latitud = None
            obj.longitud = None
            print(obj)
            obj.save()                
 
    print('Finished updating coordinates')


@app.task
def start_process(id, c, d):
    _, created = Status.objects.update_or_create(
        id_task = id,
        command = c,
        status = 'O',
        date = d,
        elapsed_time = 0
        )      

@app.task
def finish_process(id, time):
    Status.objects.filter(id_task=id).update(
        status = 'C',
        elapsed_time = time,
        )      

@app.task
def failed_process(id, time):
    Status.objects.filter(id_task=id).update(
        status = 'F',
        elapsed_time = time+1,
        )  


@app.task(bind=True)
def upload_sample_hospital(self, data):
    start = datetime.now()
    id = self.request.id
    command = 'UploadHospital'
    
    start_process.delay(id, command, start.strftime('%Y-%m-%d %H:%M:%S'))
    
    print(f'Starting hospital sample upload... (Task ID: {id})')
    try:
        substitute = 'id_uvigo;fecha_entrada_uv;id_hospital;numero_envio;id_tube;id_sample;collection_date;id_patient;gender;age;location;cp;ct_orf1ab;ct_gen_e;ct_gen_n;ct_rdrp;hospitalizacion;uci;fecha_sintomas;fecha_diagnostico;observaciones'
        fieldnames = substitute.split(';')
        io_string = io.StringIO(data)
        dialect = csv.Sniffer().sniff(io_string.readline())
        # io_string.seek(0)      
        reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect) 
        
        repl = str.maketrans("ÁÉÍÓÚ","AEIOU") # para quitar acentos
        for line in reader:
            codigo = line['cp']
            loc = line['location']
            id_linea = line['id_uvigo']
            age = line['age']
            patient = str(line['id_patient'])
            orf1ab = line['ct_orf1ab'].replace(',','.')
            gen_e = line['ct_gen_e'].replace(',','.')
            gen_n = line['ct_gen_n'].replace(',','.')
            rdrp = line['ct_rdrp'].replace(',','.')
                
            if orf1ab == '': orf1ab = 0.00
            if gen_e == '': gen_e = 0.00
            if gen_n == '': gen_n = 0.00
            if rdrp == '': rdrp = 0.00
                
            try: 
                collection_d = datetime.strptime(line['collection_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
            except: pass
            try: 
                f_sintomas = datetime.strptime(line['fecha_sintomas'], '%d/%m/%Y').strftime('%Y-%m-%d')
            except: pass
            try: 
                f_diagnostico = datetime.strptime(line['fecha_diagnostico'], '%d/%m/%Y').strftime('%Y-%m-%d')
            except: pass
            try: 
                f_entrada_uv = datetime.strptime(line['fecha_entrada_uv'], '%d/%m/%Y').strftime('%Y-%m-%d')            
            except: pass
            
            try: 
                int(codigo)
            except: codigo = 0
                
            try:
                int(age)
            except: age = 0
                
            if not Region.objects.filter(cp=codigo, location=loc).exists():
                lat, long = coords(str(codigo)+' '+ loc + ' ' + 'SPAIN')
                _, created = Region.objects.update_or_create(
                        cp = int(codigo),
                        location = loc.upper().translate(repl),
                        latitude = lat,
                        longitude = long
                    )
                
            if not Sample.objects.filter(id_uvigo=id_linea).exists():
                _, created = Sample.objects.update_or_create(
                        id_uvigo = id_linea,
                        id_accession = 'NULL',
                        id_region = Region.objects.get(cp=codigo, location=loc.upper().translate(repl)).pk,
                        original_name = 'NULL',
                        age = age,
                        gender = line['gender'][:1].upper(),
                        patient_status = line['hospitalizacion'],
                        originating_lab = 'UVIGO',
                        collection_date = collection_d,
                        additional_info = line['observaciones']
                    )
                
            if not SampleMetaData.objects.filter(id_uvigo=id_linea).exists():
                _, created = SampleMetaData.objects.update_or_create(
                        id_uvigo = id_linea,
                        id_patient = patient,
                        numero_envio = line['numero_envio'],
                        id_tube = line['id_tube'],
                        id_sample = line['id_sample'],
                        hospitalizacion = line['hospitalizacion'][:1], 
                        uci = line['uci'][:1],
                        ct_orf1ab = orf1ab,
                        ct_gen_e = gen_e,
                        ct_gen_n = gen_n,
                        ct_redrp = rdrp,
                        fecha_sintomas = f_sintomas,
                        fecha_diagnostico = f_diagnostico,
                        fecha_entrada_uv = f_entrada_uv
                    ) 
        finish = datetime.now()
        elapsed_time = finish - start
        finish_process(id, elapsed_time.seconds)
        print(f'Sample upload finished! (Elapsed time (s): {elapsed_time.seconds} (Task ID: {id})')
    except:
        finish = datetime.now()
        elapsed_time = finish - start
        print(f'Sample upload failed! (Elapsed time (s): {elapsed_time.seconds} (Task ID: {id})')
        failed_process.delay(id, elapsed_time.seconds)






def upload_sample_gisaid():
    pass

def upload_sample_transmit():
    pass