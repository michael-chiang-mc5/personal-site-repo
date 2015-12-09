from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import *
from django.db.models import Q
import pdb
from MCBase.views import *
import MCEditor

def upvote_toggle(request,post_pk):
    post = MCPost.objects.get(pk=post_pk)
    # clear upvote if user already upvoted
    if post.upvoters.filter(id=request.user.pk).exists():
        post.upvoters.remove(request.user)
    # upvote if user has not already upvoted
    else:
        post.upvoters.add(request.user)
        post.downvoters.remove(request.user)
    return HttpResponse(post.score())

def downvote_toggle(request,post_pk):
    post = MCPost.objects.get(pk=post_pk)
    # clear downvote if user already downvoted
    if post.downvoters.filter(id=request.user.pk).exists():
        post.downvoters.remove(request.user)
    # downvote if user has not already downvoted
    else:
        post.downvoters.add(request.user)
        post.upvoters.remove(request.user)
    return HttpResponse(post.score())

def editPost_editor(request):
    # this is form data that will be submitted to submit_url
    post_pk = int(request.POST.get("post-pk"))
    next_url = request.POST.get("next-url")
    serialized_form_data = serialize_json({'post_pk':post_pk,'next_url':next_url})
    # other template variables
    submit_url = reverse('MCPost:editPost')
    header = request.POST.get("header")
    initial_text = MCPost.objects.get(pk=post_pk).get_most_recent_text()
    # create editor
    html = MCEditor.views.editor(request,submit_url,serialized_form_data,header,initial_text)
    return html
def editPost(request):
    # get POST variables
    post_text = request.POST.get("post-text")
    serialized_form_data = request.POST.get("serialized-form-data")
    form_data = deserialize_json_string(serialized_form_data)
    post_pk = int(form_data["post_pk"])
    next_url = form_data["next_url"]
    # check to make sure user requesting edit is original author or superuser
    post = MCPost.objects.get(pk=post_pk)
    original_user_pk = post.user.pk
    if not request.user.is_superuser and original_user_pk != request.user.pk:
        return HttpResponse("invalid user requesting edit")
    # do edit and save
    post.edit(post_text,request.user.pk)
    post.save()
    return HttpResponseRedirect(next_url)

def replyPost_editor(request):
    # this is form data that will be submitted to submit_url
    mother_pk = request.POST.get("mother-pk")
    next_url = request.POST.get("next-url")
    serialized_form_data = serialize_json({'mother_pk':mother_pk,'next_url':next_url})
    # other template variables
    submit_url = reverse('MCPost:replyPost')
    header = request.POST.get("header")
    initial_text = ''
    # create editor
    html = MCEditor.views.editor(request,submit_url,serialized_form_data,header,initial_text)
    return html
def replyPost(request,append_anchor=True):
    # get POST variables
    post_text = request.POST.get("post-text")
    serialized_form_data = request.POST.get("serialized-form-data")
    form_data = deserialize_json_string(serialized_form_data)
    mother_pk = int(form_data["mother_pk"])
    next_url = form_data["next_url"]
    # create post
    mother = MCPost.objects.get(pk=mother_pk)
    post = MCPost(user=request.user,mother=mother,node_depth=mother.node_depth+1)
    post.edit(post_text,request.user.pk)
    post.save()
    post.upvoters.add(request.user) # user automatically upvotes his own post
    post.save()
    # return
    if append_anchor:
        next_url += '#post-' + str(post.pk)
    return HttpResponseRedirect(next_url)

#TODO: This might not be needed
def index(request):
    posts = MCPost.objects.filter(~Q(node_depth = 0))
    context={'posts':posts,}
    return render(request, 'MCPost/index.html', context)

# TODO: This might not be needed
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





#
def get_ordered_tree(base_post,exclude_base_post_from_results=True):
    # get list of all posts in tree
    posts = base_post.get_subtree()

    # Get children of all posts in tree. childrenIdx_list[i] gives the indices of children of posts[i]
    childrenIdx_list = [None] * len(posts)
    for j,post in enumerate(posts):
        children = post.mcpost_set.all()
        children_idx = []
        for child in children:
            child_idx = None
            for i,p in enumerate(posts):
                if child.pk is p.pk:
                    child_idx = i
                    break
            children_idx.append(child_idx)
        childrenIdx_list[j] = children_idx

    # first element of posts is the base node (see implementation of get_subtree)
    idx_baseNode = 0

    # get ordered post indices using recursion
    ordered_indices = get_ordered_tree_recursive(idx_baseNode, posts, childrenIdx_list)

    # get ordered posts
    ordered_posts = []
    for i,post in enumerate(ordered_indices):
        if type(ordered_indices[i]) is str: # ordered_indices[i] is 'in', 'out' representing indent, dedent
            ordered_posts.append(ordered_indices[i])
        else:
            ordered_posts.append(posts[ ordered_indices[i] ])

    if exclude_base_post_from_results:
        ordered_posts = ordered_posts[2:-1] # exclude first entry (dummy post) along with indents/dedents

    # return ordered posts
    return ordered_posts

# Returns a list of indices corresponding to an ordered post_list
# ordered[i] = j means that the jth element of post_list belongs in slot i of ordered list
# ordered[i] = 'in-*' or 'out-*' is an indent or dedent
def get_ordered_tree_recursive(node_idx, post_list, childrenIdx_list, withIndents=True):
    children_indices = childrenIdx_list[node_idx]
    num_children = len(children_indices)

    if num_children is 0:
        if withIndents:
            return ['in-'+str(post_list[node_idx].node_depth),node_idx,'out-'+str(post_list[node_idx].node_depth)]
        else:
            return [node_idx]
    else:
        # create tuple list [ (aggregateScore, index), ...] which is sorted by aggregateScore
        tup = [None] * len(children_indices)
        for i,child_idx in enumerate(children_indices):
            score = post_list[child_idx].score()
            tup[i] = (score,child_idx)
        tup = sorted(tup, reverse=True)
        if withIndents:
            ordered = ['in-'+str(post_list[node_idx].node_depth),node_idx]
        else:
            ordered = [node_idx]
        for t in tup:
            score = t[0]
            child_idx = t[1]
            o = get_ordered_tree_recursive(child_idx,post_list,childrenIdx_list,withIndents)
            if withIndents:
                ordered = ordered + o
            else:
                ordered = ordered + o
        if withIndents:
            ordered = ordered + ['out-'+str(post_list[node_idx].node_depth)]
        return ordered

def deletePost(request):
    pass

def post_context(request,post_pk):
    pass
