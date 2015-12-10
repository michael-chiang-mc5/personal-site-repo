from django.shortcuts import render
from django.http import HttpResponse
import MCCitation
import datetime
import math
from .models import *

def list_all(request):
    papersOfTheWeek = PaperOfTheWeek.objects.order_by('order')
    citations = []
    for paperOfTheWeek in papersOfTheWeek:
        citations.append(paperOfTheWeek.citation)
    context = {'citations': citations}
    return render(request, 'MCPaperHighlight/list_all.html', context)

def frontpage(request):
    citation,dummy = getCurrentPaperHighlight()
    context = {'citation': citation}
    return render(request, 'MCPaperHighlight/frontpage.html', context)

# TODO: check that number of Papers of the Week does not exceed weeks elapsed
# return1 = MCPubmedCitation object corresponding to the current Paper Highlight
# return2 = current index
def getCurrentPaperHighlight():
    t0 = datetime.date(2000, 1, 1)
    today = datetime.date.today()
    days_elapsed = (today-t0).days
    weeks_elapsed = math.floor(days_elapsed / 7)
    num_papersOfTheWeek = len(PaperOfTheWeek.objects.all())
    if num_papersOfTheWeek == 0:
        return 0,0
    else:
        current_index = (weeks_elapsed + Scheduler.objects.all()[0].offset) % num_papersOfTheWeek
        citation_pk = PaperOfTheWeek.objects.order_by('order')[current_index].citation.pk
        citation = MCPubmedCitation.objects.get(pk=citation_pk)
        return citation,current_index

# admin interface to set paper of the week
def admin(request):
    # add/remove/change order of  citations from weekly rotation if user submits form
    if request.method == 'POST':
        addOrRemove = request.POST.get('addOrRemove')
        citation_pk = request.POST.get('citation_pk')
        order = request.POST.get('order')
        offset = request.POST.get('offset')

        # order is what order in the weekly rotation an added citation should be inserted into.
        # If order is not specified, add to the end of the list
        if order=="":
            sorted_citations = PaperOfTheWeek.objects.order_by('-order')  # TODO: sort is inefficient, better to find min
            if len(sorted_citations) == 0:
                order = 0
            else:
                order = sorted_citations[0].order + 1
        # Add a citation to the weekly rotation
        if addOrRemove == "add":
            scheduler = Scheduler.objects.all()[0]
            c = MCPubmedCitation.objects.get(pk=citation_pk)
            new_pow_entry = PaperOfTheWeek(citation = c, scheduler=scheduler, order=order)
            new_pow_entry.save()
        # Remove a citation from the weekly rotation
        elif addOrRemove == "remove":
            c = MCPubmedCitation.objects.get(pk=citation_pk)
            p = PaperOfTheWeek.objects.filter(citation=c)
            p.delete()
        # offset is a number that lets us "dial" the weekly rotation
        # if offset is specified, then set Scheduler.offset so that the
        #    current paper of the week has an order that is cloest to specified offset
        if offset!="":
            paperOfTheWeek_list = PaperOfTheWeek.objects.order_by('order')
            # find index (idx) of citation with order (o) closest to offset
            idx = 0
            diff_storage = float('inf')
            for i,p in enumerate(paperOfTheWeek_list):
                o = p.order
                diff = abs(o - float(offset))
                if diff<diff_storage:
                    diff_storage = diff
                    idx = i
            # determine modulus offset
            dummy,currentIdx = getCurrentPaperHighlight()
            if idx > currentIdx:
                scheduler = Scheduler.objects.all()[0]
                scheduler.offset = scheduler.offset + (idx-currentIdx)
                scheduler.save()
            elif idx < currentIdx:
                scheduler = Scheduler.objects.all()[0]
                scheduler.offset = scheduler.offset - (currentIdx-idx)
                scheduler.save()

    # check if scheduler exists. If not, create one
    if len(Scheduler.objects.all()) == 0:
        scheduler = Scheduler()
        scheduler.save()
    # Make it so that PaperOfTheWeek orders are integers
    paperOfTheWeek_list = PaperOfTheWeek.objects.order_by('order')
    for i,p in enumerate(paperOfTheWeek_list):
        p.order = i
        p.save()
    # get order of current paper of the week
    dummy,idx = getCurrentPaperHighlight()
    if idx==0: # there is no current paper of the week
        currentOrder=0
    else:
        currentOrder = paperOfTheWeek_list[idx].order

    # this is a list of all citations not used in Papers of the Week
    nonPaperOfTheWeek_list = MCPubmedCitation.objects.exclude(paperoftheweek__in=paperOfTheWeek_list)
    context = {'paperOfTheWeek_list': paperOfTheWeek_list, 'nonPaperOfTheWeek_list':nonPaperOfTheWeek_list, 'currentOrder':currentOrder}
    return render(request, 'MCPaperHighlight/admin.html', context)
