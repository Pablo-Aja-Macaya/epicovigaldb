from django.shortcuts import render
from .models import Task
from django.contrib.auth.decorators import login_required
from upload.models import Sample
from collections import Counter

def sample_origin_graph():
    hospital_list = []
    for i in Sample.objects.all():
        hospital_list.append(i.hospital_id())
    
    queryset = []
    hospital_count = Counter(i['id_uvigo'] for i in hospital_list)
    for k,v in hospital_count.items():
        queryset.append({'hospital':k, 'number':int(v)})
    return queryset

#@login_required(login_url="/accounts/login")
def home(request):
    if request.user.is_authenticated:
        tasks = Task.objects
        url = 'tasks/home.html'
        return render(request, url, {'tasks':tasks})
    else:
        tasks = Task.objects.filter(show_to='all')
        url = 'tasks/visitor_home.html'
        return render(request, url, {'tasks':tasks, 'hospitals':sample_origin_graph()})







