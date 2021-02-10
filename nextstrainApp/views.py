
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt

#@login_required(login_url="/accounts/login") 
@xframe_options_exempt
def auspice(request):  
    return render(request, 'nextstrainApp/auspice.html')