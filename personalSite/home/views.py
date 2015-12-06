from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'navbasdr_home':True}
    #return HttpResponse("home")
    return render(request, 'home/index.html', context)
