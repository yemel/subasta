# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from web.models import ITEMS

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=75)

# Create your views here.
def all_auctions(request):
    return render(request, 'all.html', {'items': ITEMS})

def active_auctions(request):
    return render(request, 'active.html', {'items': ITEMS[:3]})

def item(request, id=None):
    item = ITEMS[int(id) - 1]
    return render(request, 'item.html', {'item': item, 'logged': request.session.get('logged')})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            request.session['logged'] = 'TRUE'
            return HttpResponseRedirect('/item/' + request.GET.get('id', 1))
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def success(request):
    return render(request, 'success.html')