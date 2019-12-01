# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session

from web.models import Product, Bid, User, Donation

class RegisterForm(forms.Form):
    pingo = forms.CharField(max_length=100)
    wango = forms.CharField(max_length=20)
    tacho = forms.EmailField(max_length=75)

def get_user(request):
    user_id = request.session.get('user')
    return user_id and User.objects.get(id=user_id) or None

def get_total_donations():
    donation, _ = Donation.objects.get_or_create(id=1)
    return donation.total() + sum([p.total_price() for p in Product.objects.all()])

def all_auctions(request):
    user = get_user(request)
    return render(request, 'all.html', {'items': Product.objects.order_by('id'), 'usr': user})

def active_auctions(request):
    user = get_user(request)
    items = Product.objects.filter(bid__user=user).distinct().order_by('id')
    return render(request, 'active.html', {'items': items, 'usr': user})

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

def register(request):
    user = get_user(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                full_name=form.cleaned_data['pingo'],
                phone=form.cleaned_data['wango'],
                email=form.cleaned_data['tacho']
            )
            request.session['user'] = user.id
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
            return HttpResponseRedirect('/donations')

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
        return HttpResponseRedirect('/status')
    
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