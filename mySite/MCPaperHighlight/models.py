from django.db import models
from MCCitation.models import *

# An object of this class stores an ordered list of citations. Used to determine the "Paper of the Week"
class Scheduler(models.Model):
    citation_list = models.ManyToManyField(MCPubmedCitation, through='PaperOfTheWeek')
    offset = models.PositiveIntegerField(default=0)

class PaperOfTheWeek(models.Model):
    citation = models.ForeignKey(MCPubmedCitation)
    order = models.FloatField()
    scheduler = models.ForeignKey(Scheduler)
    def __str__(self):
        return str(self.citation) + ", order=" + str(self.order)
