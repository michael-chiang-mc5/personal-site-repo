from django.shortcuts import render
from django.http import HttpResponse
from MCCitation.models import *
from .models import *
from MCPost.views import *


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
    base_posts = discussion.get_associated_posts()

    # get post tree
    post_trees = []
    for base_post in base_posts:
        post_tree = get_ordered_tree(base_post)
        post_trees.append(post_tree)

    # zip
    zipped = zip(threads,base_posts,post_trees)

    context = {'current_thread':int(current_thread),'citation':citation,'zipped':zipped,'threads':threads}
    return render(request, 'MCDiscussCitation/detail.html', context)
