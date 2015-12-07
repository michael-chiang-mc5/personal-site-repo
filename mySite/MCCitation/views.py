from django.shortcuts import render
from .models import *
import json
from django.http import HttpResponse
import math
from django.core.urlresolvers import reverse

def index(request):
    citations = MCPubmedCitation.objects.all()
    context = {'citations':citations}
    return render(request, 'MCCitation/index.html', context)

def addCitation(request):
    citation_serialized = request.POST['citation_serialized']
    citation = MCPubmedCitation()
    citation.deserialize(citation_serialized)
    citation_pk = citation.save_if_unique()
    # Return url to new citation detail page
    new_citation_url = reverse('MCCitation:detail',args=[citation_pk,0])
    return HttpResponse(new_citation_url)

def import_from_pubmed(request,page):
    # hard-coded parameters
    results_per_page = 10
    max_number_of_pages = 20

    # initialize
    is_fresh_search = True
    search_bar_placeholder = "Search pubmed ..."
    current_page = 0
    total_number_search_results = 0
    total_pages = 0
    citations = []

    # client has passed us POST data containing Pubmed xml
    # we will create list of citation objects from POST data and pass it back
    if request.method == 'POST':
        is_fresh_search = False
        search_bar_placeholder = request.POST.get("search_bar_placeholder")
        current_page = request.POST.get("goto_page")
        total_number_search_results = int(request.POST.get("pubmed_return_num_results"))
        total_pages = min(math.ceil(total_number_search_results/results_per_page),max_number_of_pages)
        json_str = request.POST.get("pubmed_return_json_str")
        #save_object(json_str, 'deleteMe.pkl')
        citations = deserialize_json_string(json_str)

    #context = {'navbar':'search','is_search_results':True,'citations':citations,'search_bar_placeholder':search_bar_placeholder,'total_pages':total_pages,'current_page':current_page,'results_per_page':results_per_page}
    context = {'is_fresh_search':is_fresh_search, \
               'search_bar_placeholder':search_bar_placeholder, \
               'current_page':current_page, \
               'total_pages':total_pages, \
               'citations':citations, \
               'results_per_page':results_per_page, \
               'citation_is_not_saved':True}
    return render(request, 'MCCitation/import_from_pubmed.html', context)

# This function takes a serialized json string containing pubmed data, then
# returns a list of MCPubmedCitation objects. This function does not save
# MCPubmedCitation objects.
def deserialize_json_string(json_str):
    json_object = json.loads(json_str)
    try:
        articles_json = json_object['PubmedArticle']
    except: # 0 citations in search results
        citations = []
    else: # more than 0 articles in the search results
        try:  # more than 1 article in search result
            citations = []
            for article_json in articles_json:
                citation = MCPubmedCitation()
                citation.parse_pubmedJson(article_json)
                citations.append(citation)
        except: # exactly one article in search results
            citations = []
            citation = MCPubmedCitation()
            citation.parse_pubmedJson(articles_json)
            citations.append(citation)
    return citations

def detail(request,pk,current_thread):
    return HttpResponse("success")
