from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import *
from django.db.models import Q

def post_editor(request):
    edit_or_reply = request.POST.get("edit-or-reply")
    header = request.POST.get("header")
    next_url = request.POST.get("next-url")

    if edit_or_reply=="edit": # TODO: implement
        pass
    elif edit_or_reply=="reply": # Note that "adding" a post is technically replying to a base node post
        initial_text = ''
        mother_pk = request.POST.get("mother-pk")
        mother = MCPost.objects.get(pk=mother_pk)

    context={'edit_or_reply':edit_or_reply, \
             'header':header,'next_url':next_url, \
             'initial_text':initial_text, \
             'mother':mother, \
            }
    return render(request, 'MCPost/post_editor.html', context)

def index(request):
    posts = MCPost.objects.filter(~Q(node_depth = 0))
    context={'posts':posts,}
    return render(request, 'MCPost/index.html', context)

def createPost(request):
    # get POST variables
    post_text = request.POST.get("post-text")
    # create a root post with depth 0 with nocontent
    root_post = MCPost(node_depth=0)
    root_post.save()
    # create post
    post = MCPost(user=request.user,mother=root_post,node_depth=1)
    post.edit(post_text,request.user.pk)
    post.save()
    post.upvoters.add(request.user) # user automatically upvotes his own post
    post.save()
    return HttpResponse("success")

def replyPost(request):
    # get POST variables
    post_text = request.POST.get("post-text")
    mother_pk = int(request.POST.get("mother-pk"))
    next_url = request.POST.get("next-url")

    # create post
    mother = MCPost.objects.get(pk=mother_pk)
    post = MCPost(user=request.user,mother=mother,node_depth=mother.node_depth+1)
    post.edit(post_text,request.user.pk)
    post.save()
    post.upvoters.add(request.user) # user automatically upvotes his own post
    post.save()

    # return
    return HttpResponseRedirect(next_url)

def editPost(request):
    # get POST variables
    post_text = request.POST.get("post-text")
    post_pk = int(request.POST.get("post-pk"))

    # check to make sure user requesting edit is original author or superuser
    post = MCPost.objects.get(pk=post_pk)
    original_user_pk = post.user.pk
    if not request.user.is_superuser and original_user_pk != request.user.pk:
        return HttpResponse("invalid user requesting edit")

    # do edit and save
    post.edit(post_text,request.user.pk)
    post.save()

    return HttpResponse("success")
