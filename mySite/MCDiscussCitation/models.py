from django.db import models
from MCCitation.models import *
from MCPost.models import *

class MCThread(models.Model):
    post = models.ForeignKey(MCPost)
    order = models.PositiveIntegerField()
    name = models.TextField()
    description = models.TextField()
    discussion = models.ForeignKey(MCDiscussion)



class MCDiscussion(models.Model):
    citation = models.ForeignKey(MCPubmedCitation)
