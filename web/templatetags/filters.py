# -*- coding: utf-8 -*-

from django import template
register = template.Library()

@register.filter
def color(product, user):
    if not user:
        return 'info'

    last_bid = product.bid_set.filter(user=user).order_by('-price').first()
    if not last_bid:
        return 'info'

    winner = product.winner_bid()
    if winner and last_bid.id == winner.id:
        return 'success'
    else:
        return 'warning'

