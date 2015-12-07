from django.shortcuts import render
from django.http import HttpResponse
from MCCitation.models import *


# Check if Discussion object exists for given citation. If not, create it
def get_associated_discussion(citation_pk):
    

def detail(request,pk,current_thread):
    citation = MCPubmedCitation.objects.get(pk=pk)



    context = {'citation':citation}
    return render(request, 'MCDiscussCitation/detail.html', context)
