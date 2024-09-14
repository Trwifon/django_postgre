from datetime import datetime

from nadejda_94.records.models import Order


def get_order(order_type):
    orders = Order.objects.first()

    date = datetime.now().month
    month_dict = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
                  7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}
    current_month = month_dict[date]
    db_month = orders.month

    counter = 0
    if order_type == 'A':
        counter = orders.al_counter
    elif order_type == 'G':
        order_type = 'C'
        counter = orders.glass_counter
    elif order_type == 'P':
        counter = orders.pvc_counter
    else:
        return ''

    if current_month != db_month:
        orders.month = current_month
        orders.al_counter, orders.glass_counter, orders.pvc_counter = 1, 1, 1
        orders.save()
        counter = 1

    return f"{order_type}-{current_month}-{counter}"


def update_order(order_type):
    orders = Order.objects.first()

    if order_type == 'A':
        orders.al_counter += 1
    elif order_type == 'G':
        orders.glass_counter += 1
    elif order_type == 'P':
        orders.pvc_counter += 1

    orders.save()


def get_close_balance(partner_id, order_type, open_balance, amount):
    if partner_id == 1 or partner_id == 2:
        return 0

    if order_type in ['C', 'B']:
        return int(open_balance) + int(amount)
    else:
        return int(open_balance) - int(amount)
