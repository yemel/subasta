import gspread
from web.models import Product

def export():
    gc = gspread.service_account(filename='firebase-key.json')
    sheet = gc.open_by_key('1d3fZgI_POuC5Yg9SpJ1kcVJ8ArYvL0HdwaBAzfOGMiw')
    ws = sheet.worksheet('Base de Datos')

    for row, p in enumerate(Product.objects.order_by('id'), start=2):
        bid = p.winner_bid()
        current_price = bid and bid.price or 0
        full_name = bid and bid.user.full_name or ''
        phone = bid and bid.user.phone or ''
        email = bid and bid.user.email or ''
        ws.update(
            'A%s:I%s' % (row, row),
            [[
                p.id, p.order, p.name, p.description, p.start_price,
                current_price, full_name, phone, email
            ]]
        )
