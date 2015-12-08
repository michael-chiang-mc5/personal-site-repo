from django.shortcuts import render
from django.http import HttpResponse
from MCCitation.models import *
from .models import *


# Check if Discussion object exists for given citation. If not, create it
def get_associated_discussion(citation_pk):
    try:
        citation=MCPubmedCitation.objects.get(pk=citation_pk)
        discussion = MCDiscussion.objects.get(citation=citation)
    except:
        citation = MCPubmedCitation.objects.get(pk=citation_pk)
        discussion = MCDiscussion(citation=citation)
        discussion.save()
        discussion.create_associated_threads()
        return discussion
    else:
        return discussion

def detail(request,citation_pk,current_thread):
    citation = MCPubmedCitation.objects.get(pk=citation_pk)
    discussion = get_associated_discussion(citation_pk)
    threads = discussion.get_associated_threads()
    posts = discussion.get_associated_posts()


    context = {'current_thread':int(current_thread),'citation':citation,'threads':threads,'posts':posts}
    return render(request, 'MCDiscussCitation/detail.html', context)
