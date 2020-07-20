# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    last_login = models.DateTimeField(null=True)

    def name(self):
        return self.full_name.split()[0]

    def __unicode__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    image = models.URLField(max_length=200)
    image_big = models.URLField(max_length=200, null=True)
    start_price = models.IntegerField()
    segment = models.IntegerField(null=True)
    order = models.IntegerField(default=1)

    def winner_bid(self):
        return self.bid_set.order_by('-price', 'created').first()

    def price(self):
        bid = self.winner_bid()
        return bid and bid.price or self.start_price

    def total_price(self):
        bid = self.winner_bid()
        return bid and bid.price or 0

    def winners(self):
        all_bids = self.bid_set.order_by('-price')
        bids = []
        for bid in all_bids:
            if bid.user_id not in [b.user_id for b in bids]:
                bids.append(bid)
                if len(bids) == 3:
                    return bids
        return bids

    def __unicode__(self):
        return self.name

class Bid(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '$%s -> %s' % (self.price, self.product)

class Donation(models.Model):
    enabled = models.BooleanField(default=True)
    raffle = models.PositiveIntegerField(default=0)
    auction_1 = models.PositiveIntegerField(default=0)
    auction_2 = models.PositiveIntegerField(default=0)
    auction_3 = models.PositiveIntegerField(default=0)
    auction_4 = models.PositiveIntegerField(default=0)
    subscriptions = models.PositiveIntegerField(default=0)
    others = models.PositiveIntegerField(default=0)

    def reset(self):
        self.enabled = True
        self.raffle = 0
        self.auction_1 = 0
        self.auction_2 = 0
        self.auction_3 = 0
        self.auction_4 = 0
        self.subscriptions = 0
        self.others = 0

    def total(self):
        return sum([self.raffle, self.auction_1, self.auction_2, self.auction_3, self.auction_4, self.subscriptions, self.others])