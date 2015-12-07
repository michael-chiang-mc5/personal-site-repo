from django.shortcuts import render
from .models import *
import json
from django.http import HttpResponse

def index(request):
    return HttpResponse("success")

def addCitation(request):
    return HttpResponse("success!")

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
