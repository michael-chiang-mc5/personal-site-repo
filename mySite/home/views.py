from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {'home':True}
    return render(request, 'MCHome/index.html', context)
