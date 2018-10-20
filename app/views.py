# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.core import serializers
import simplejson
from django.http import HttpResponse, JsonResponse
import xlsxwriter
import os

from app.models import *
# Create your views here.

def ViewPolls(request):
    poll = Polls.objects.extra(select={'counts':'SELECT MAX(now_count) FROM app_pollperson WHERE app_pollperson.polls_id = app_polls.id'})
    const = {
        'poll':poll,
        'page':'app/index.html',
    }
    return render_to_response("app/layout.html",const)

def ViewPollPerson(request,poll):
    poll = PollPerson.objects.filter(polls__id=poll)
    res = []
    for pp in poll:
        res.append({'pid':pp.id,'polls':pp.polls.id,'fio':pp.person.fio,'foto':pp.person.foto.url})
    return JsonResponse(res, safe=False)

def ViewPollPersonClose(request,poll):
    poll = PollPerson.objects.filter(polls__id=poll)
    res = []
    for pp in poll:
        res.append({'pid':pp.id,'polls':pp.polls.id,'fio':pp.person.fio,'foto':pp.person.foto.url,'count':pp.now_count})
    return JsonResponse(res, safe=False)


def AddVotePerson(request,pp):
    pp = PollPerson.objects.get(pk=pp)
    pp.now_count = pp.now_count + 1
    pp.save()

    return HttpResponse('Ok')

def CreateXLSX(request,poll):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILL = 'static/xlsx/'+'Detail'+str(poll)+'.xlsx'
    PATH = os.path.join(BASE_DIR, FILL)
    fill = xlsxwriter.Workbook(PATH)
    sheet = fill.add_worksheet()
    pp = PollPerson.objects.filter(polls__id=poll)
    row = 0
    for i in pp:
        sheet.write(row,1,i.person.fio)
        sheet.write(row,2,i.polls.name)
        sheet.write(row,3,i.now_count)
        row = row + 1
    fill.close()
    const = {'file':FILL}
    return JsonResponse(const)