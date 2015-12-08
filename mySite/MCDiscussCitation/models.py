from django.db import models
from MCCitation.models import *
from MCPost.models import *
from MCPost.views import *

class MCDiscussion(models.Model):
    citation = models.ForeignKey(MCPubmedCitation)

    # MCDiscussion should be saved prior to running this
    def create_associated_threads(self):
        titles = ["Explain Like I'm Five","Methodology","Results","Historical Context"]
        descriptions = ["Easy to understand summary of the paper",
                               "Description of innovative methodologies",
                               "Description of main results of the paper",
                               "How does the paper fit into the pre-existing literature"]
        ordering = [1,2,3,4]
        for title,description,order in zip(titles,descriptions,ordering):
            thread = MCDiscussionThread(order=order,title=title,description=description,discussion=self)
            thread.init_post()
            thread.save()

    def get_associated_threads(self):
        threads = MCDiscussionThread.objects.filter(discussion=self).order_by('order')
        return threads

    def get_associated_posts(self):
        threads = self.get_associated_threads()
        posts = []
        for thread in threads:
            posts.append(thread.get_associated_post())
        return posts

class MCDiscussionThread(models.Model):
    post = models.ForeignKey(MCPost)
    order = models.PositiveIntegerField()
    title = models.TextField()
    description = models.TextField()
    discussion = models.ForeignKey(MCDiscussion)

    def get_header(self):
        return self.title + " - " + self.description

    def init_post(self):
        post = MCPost(text_history="base node MCPost",node_depth=0)
        post.save()
        self.post = post

    def get_associated_post(self):
        return self.post

    def get_number_of_posts(self):
        return len(MCPost.objects.filter(mother=self.post))

    def get_associated_post_pk(self):
        return self.post.pk

    def get_post_tree(self):
        post_tree = get_ordered_tree(self.post)
        return post_tree
