# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

from web.models import Product, Bid, User

class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=75)

def get_user(request):
    user_id = request.session.get('user')
    return user_id and User.objects.get(id=user_id) or None

def all_auctions(request):
    user = get_user(request)
    return render(request, 'all.html', {'items': Product.objects.order_by('id'), 'usr': user})

def active_auctions(request):
    user = get_user(request)
    items = Product.objects.filter(bid__user=user).distinct().order_by('id')
    return render(request, 'active.html', {'items': items, 'usr': user})

def item(request, id=None):
    item = Product.objects.get(id=id)
    user = get_user(request)

    if request.method == 'POST':
        bid_price = int(request.POST.get('options'))

        if bid_price > item.price():
            bid = Bid.objects.create(user=user, product=item, price=bid_price)
            return HttpResponseRedirect('/success/%s' % bid.id)

    return render(request, 'item.html', {'item': item, 'usr': user})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(**form.cleaned_data)
            request.session['user'] = user.id
            return HttpResponseRedirect('/item/' + request.GET.get('id', 1))
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def success(request, id=None):
    bid = Bid.objects.get(id=id)
    return render(request, 'success.html', {'bid': bid})