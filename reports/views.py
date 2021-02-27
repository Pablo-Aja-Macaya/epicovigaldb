from django.shortcuts import render

# Create your views here.
def tmp(request):
    return render(request, 'reports/reports_list.html')

def tmp2(request, id):
    return render(request, 'reports/report.html', {'id':id})