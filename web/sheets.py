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
        from_email='Mensajeros de la Paz <mensajeros@misubasta.org>', # request.user.get_full_name()
        recipient_list=[user.email],
        context=merge_data
    )