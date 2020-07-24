import gspread
from web.models import Product

def export_winners():
    gc = gspread.service_account(filename='firebase-key.json')
    sheet = gc.open_by_key('1d3fZgI_POuC5Yg9SpJ1kcVJ8ArYvL0HdwaBAzfOGMiw')
    ws = sheet.worksheet('Ganadores')

    for row, p in enumerate(Product.objects.order_by('id'), start=2):
        bid = p.winner_bid()
        current_price = bid and bid.price or 0
        full_name = bid and bid.user.full_name or ''
        phone = bid and bid.user.phone or ''
        email = bid and bid.user.email or ''
        ws.update(
            'A%s:G%s' % (row, row),
            [[
                p.order, p.name, p.start_price,
                current_price, full_name, phone, email
            ]]
        )


from django.core.mail import send_mail

def send_email():
    send_mail(
        "Hoy cierra la subasta!",
        "Entrá a ver los productos que tenemos!",
        "Mensajeros de la Paz <mensajeros@misubasta.org>",
        ["angel.jardi@gmail.com"],
        html_message='<html><body>Entrá a ver los productos que tenemos!.<br/><a href="https://mensajeros.misubasta.org">Ir a la subasta</a></body></html>'
    )


from templated_email import send_templated_mail

def send_today(user):
    merge_data = {
        'FIRST_NAME': user.name()
    }
    send_templated_mail(
        template_name='today',
        from_email='Mensajeros de la Paz <mensajeros@misubasta.org>',
        recipient_list=[user.email],
        context=merge_data
    )



def send_outbid(bid):
    merge_data = {
        'FIRST_NAME': bid.user.name(),
        'TITLE': bid.product.name,
        'PRICE': bid.price,
        'PID': bid.product.id,
    }
    send_templated_mail(
        template_name='outbid',
        from_email='Mensajeros de la Paz <mensajeros@misubasta.org>',
        recipient_list=[bid.user.email],
        context=merge_data
    )

def send_outbid_for_product(product):
    bids = product.bid_set.order_by('-price')
    if not bids: return
    users = [bids[0].user]

    for bid in bids[1:]:
        if bid.user in users:
            continue
        users.append(bid.user)
        send_outbid(bid)
        print('Sending outbid to', bid.user.name(), bid.price)


def send_winner(bid):
    merge_data = {
        'FIRST_NAME': bid.user.name(),
        'TITLE': bid.product.name,
        'PRICE': bid.price,
    }
    send_templated_mail(
        template_name='winner',
        from_email='Mensajeros de la Paz <mensajeros@misubasta.org>',
        recipient_list=[bid.user.email],
        context=merge_data
    )

def send_all_winners():
    for p in Product.objects.all():
        bid = p.winner_bid()
        if bid:
            send_winner(bid)


def send_donate(bid):
    merge_data = {
        'FIRST_NAME': bid.user.name(),
        'PRICE': bid.price,
        'MP_LINK': 'https://mercadopago.com',
    }
    send_templated_mail(
        template_name='donate',
        from_email='Mensajeros de la Paz <mensajeros@misubasta.org>',
        recipient_list=[bid.user.email],
        context=merge_data
    )