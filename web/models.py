# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def name(self):
        return self.full_name.split()[0]

    def __unicode__(self):
        return self.full_name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    image = models.URLField(max_length=200)
    start_price = models.IntegerField()

    def winner_bid(self):
        return self.bid_set.order_by('-price', 'created').first()

    def price(self):
        bid = self.winner_bid()
        return bid and bid.price or self.start_price

    def total_price(self):
        bid = self.winner_bid()
        return bid and bid.price or 0

    def __unicode__(self):
        return self.name

class Bid(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '$%s -> %s' % (self.price, self.product)
