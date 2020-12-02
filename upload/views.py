from django.shortcuts import render
# from .models import Region, Sample, OurSampleCharacteristic
# from .models import upload_sample_hospital
from .tasks import upload_csv_task, upload_sample_hospital
from django.contrib.auth.decorators import login_required

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
    import io
    def check_file():
        pass     
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        data = uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data)
        if request.POST.get('origin') == 'hospital':
            upload_sample_hospital.delay(data)
            # upload_sample_hospital(io_string)
            # upload_csv_task.delay(1)
            return render(request, 'upload/csv.html', {'message':'Uploading in the back!'})
        
        else:
            return render(request, 'upload/csv.html',{'warning':'Origin not implemented yet'})

    else:
        return render(request, 'upload/csv.html',{'message':'Something went wrong.'})
    
    

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
            
#             if not OurSampleCharacteristic.objects.filter(id_uvigo=id_linea).exists():
#                 _, created = OurSampleCharacteristic.objects.update_or_create(
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
    