# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth import login

from web.models import Product, Bid, User, Donation


class RegisterForm(forms.Form):
    pingo = forms.CharField(max_length=100)
    wango = forms.CharField(max_length=20)
    tacho = forms.EmailField(max_length=75)


def get_user(request):
    return None if request.user.is_anonymous() else request.user


def get_total_donations():
    donation, _ = Donation.objects.get_or_create(id=1)
    return donation.total() + sum([p.total_price() for p in Product.objects.all()])


def all_auctions(request):
    user = get_user(request)
    if user:
        active_items = Product.objects.filter(bid__user=user).distinct().order_by('id')
        other_items = Product.objects.exclude(id__in=[p.id for p in active_items]).order_by('id')
    else:
        active_items = []
        other_items = Product.objects.all()

    return render(request, 'all.html', {'active_items': active_items, 'other_items': other_items, 'usr': user})


def item(request, id=None):
    donation, _ = Donation.objects.get_or_create(id=1)
    item = Product.objects.get(id=id)
    user = get_user(request)

    if request.method == 'POST' and donation.enabled:
        bid_price = request.POST.get('options')
        bid_price = int(request.POST.get('amount')) if bid_price == "OTHER" else int(bid_price)

        if bid_price > item.price():
            bid = Bid.objects.create(user=user, product=item, price=bid_price)
            return HttpResponseRedirect('/success/%s' % bid.id)

    return render(request, 'item.html', {'item': item, 'usr': user, 'donation': donation})


def conditions(request):
    id = request.GET.get('id', None)
    return render(request, 'conditions.html', {'next': id})


def register(request):
    user = get_user(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=str(uuid.uuid4()),
                full_name=form.cleaned_data['pingo'],
                phone=form.cleaned_data['wango'],
                email=form.cleaned_data['tacho']
            )
            login(request, user)
            return HttpResponseRedirect('/item/' + request.GET.get('id', 1))
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'usr': user})


def success(request, id=None):
    bid = Bid.objects.get(id=id)
    return render(request, 'success.html', {'bid': bid})


def results(request):
    total = get_total_donations()
    return render(request, 'results.html', {'total': total})


def api_signin(request, id, microsecond):
    u = User.objects.get(id=id)
    if u.created.microsecond == int(microsecond):
        login(request, u)
    return HttpResponseRedirect('/')


def api_wining(request, id):
    user = get_user(request)
    product = Product.objects.get(id=id)
    user_bid = product.bid_set.filter(user=user).order_by('-price').first()
    winner = product.winner_bid()
    response = 1 if user_bid.id == winner.id else 0
    return HttpResponse(response, content_type="application/json")


def api_result(request):
    total = get_total_donations()
    return HttpResponse(total, content_type="application/json")


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = []

def donations(request):
    donation, _ = Donation.objects.get_or_create(id=1)
    form = DonationForm(instance=donation)
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/donaciones')

    return render(request, 'donations.html', {'form': form})

def winners(request):
    user = get_user(request)
    return render(request, 'winners.html', {'items': Product.objects.order_by('id'), 'usr': user})

def products(request):
    return render(request, 'products.html', {'items': Product.objects.order_by('id')})

def status(request):
    donation, _ = Donation.objects.get_or_create(id=1)
    user = get_user(request)
    if request.method == 'POST':
        donation, _ = Donation.objects.get_or_create(id=1)
        donation.enabled = request.POST['enabled'] == 'yes'
        donation.save()
        return HttpResponseRedirect('/subasta')
    
    return render(request, 'status.html', {'donation': donation, 'usr': user})

def reset(request):
    if request.method == 'POST':
        User.objects.all().delete()
        Session.objects.all().delete()
        donation, _ = Donation.objects.get_or_create(id=1)
        donation.reset()
        donation.save()
        return HttpResponseRedirect('/')

    return render(request, 'reset.html')