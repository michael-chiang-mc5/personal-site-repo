from django.shortcuts import render
from MCCitation.views import *
import math

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
    return render(request, 'MCJournalclub/import_from_pubmed.html', context)
