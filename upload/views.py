from django.shortcuts import render
from .models import Region
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
def region_upload(request):
    import csv, io
    
    def coords(place):
        from geopy import Nominatim
        # import time
        geolocator = Nominatim(user_agent='test')
        # time.sleep(1) 
        try:
            location = geolocator.geocode(place)
            return location.latitude,location.longitude
        except:
            return 'NULL','NULL'
           
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        data = uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data)
        
        substitute = 'id_uvigo;fecha_entrada_uv;id_hospital;numero_envio;id_tube;id_sample;collection_date;id_patient;gender;age;location;cp;ct_orf1ab;ct_gen_e;ct_gen_n;ct_rdrp;hospitalizacion;uci;fecha_sintomas;fecha_diagnostico;observaciones'
        fieldnames = substitute.split(';')
        dialect = csv.Sniffer().sniff(io_string.readline())
        # io_string.seek(0)      
        reader = csv.DictReader(io_string, fieldnames=fieldnames, dialect=dialect) 
        
        repl = str.maketrans("ÁÉÍÓÚ","AEIOU") # para quitar acentos
        for line in reader:
            codigo = line['cp']
            loc = line['location']
            try: 
                int(codigo)
            except:
                codigo = 0
                

            if not Region.objects.filter(cp=codigo, location=loc).exists():
                lat, long = coords(str(codigo)+' '+ loc + ' ' + 'SPAIN')
                _, created = Region.objects.update_or_create(
                    cp = int(codigo),
                    location = loc.upper().translate(repl),
                    latitude = lat,
                    longitude = long
                )
       
        return render(request, 'upload/csv.html',{'message':'Upload completed succesfully!'})
    else:
        return render(request, 'upload/csv.html',{'message':'Something went wrong.'})
    
    

