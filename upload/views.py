from django.shortcuts import render
from .tasks import find_coords
from django.contrib.auth.decorators import login_required
from .utils import upload_utils
import io






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
        try:
            uploaded_file = request.FILES['document']
            data = uploaded_file.read().decode('UTF-8')
            io_string = io.StringIO(data)
            if request.POST.get('origin') == 'hospital':
                #upload_sample_hospital.delay(data)
                upload_utils.upload_sample_hospital(io_string)
                #find_coords.delay() # esto se hace por detrás con celery
                return render(request, 'upload/csv.html', {'message':'Finishing coordinates in the back!'})
            else:
                return render(request, 'upload/csv.html',{'warning':'Origin not implemented yet'})
        except Exception as e:
            print(e)
            return render(request, 'upload/csv.html',{'warning':'Something went wrong (1).'})

    else:
        return render(request, 'upload/csv.html',{'message':'Something went wrong (2).'})
    





    