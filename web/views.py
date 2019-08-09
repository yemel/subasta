# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from web.models import ITEMS

# Create your views here.
def all_auctions(request):
    return render(request, 'all.html', {'items': ITEMS})

def active_auctions(request):
    return render(request, 'active.html', {'items': ITEMS[:3]})

def item(request, id=None):
    item = ITEMS[int(id) - 1]
    return render(request, 'item.html', {'item': item})