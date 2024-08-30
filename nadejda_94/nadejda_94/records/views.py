from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum, Count
from .forms import RecordForm, PartnerForm, WarehouseForm
from .models import Record, Partner, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

CURRENT_WAREHOUSE = 'O'

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
                messages.error(request, 'Този потребител не съществува')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Грешна парола')

    context = {}
    return render(request, 'login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def create_record(request):
    form = RecordForm()
    title = 'Нов запис'

    if request.method == 'POST':
        form = RecordForm(request.POST)
        form.instance.warehouse = CURRENT_WAREHOUSE

        if form.is_valid():
            partner = Partner.objects.get(id=form['partner'].value())
            partner_id = partner.id
            open_balance = partner.balance

            order_type = form.cleaned_data['order_type']

            amount = form.cleaned_data['amount']
            amount = -abs(int(amount)) if partner_id == 1 else amount

            close_balance = get_close_balance(partner_id, order_type, open_balance, amount)

            order = get_order(order_type)

            form.instance.partner = partner
            form.instance.amount = amount
            form.instance.balance = close_balance
            form.instance.order = order
            form.save()

            partner.balance = close_balance
            partner.save()

            messages.success(request, f"Записана поръчка {order} на клиент {partner} за {amount} лв.")

            return redirect('home')

    context = {'title': title, 'form': form}
    return render(request, 'choice_reports.html', context)


def home(request):
    return render(request, 'home.html')


def day_reports(request):
    form = WarehouseForm()
    title = 'Дневен отчет'

    if request.method == 'POST':
        current_warehouse = request.POST.get('warehouse')

        results = Record.objects\
            .filter(created_at=datetime.today(), warehouse=current_warehouse)\
            .order_by('id')

        total_sum = results.filter(order_type='C').aggregate(Sum('amount'))
        total = total_sum['amount__sum']
        payload = {'records': results, 'total_sum': total}

        return render(request, template_name='show_reports.html', context=payload)

    context = {'title': title, 'form': form}
    return render(request, 'choice_reports.html', context=context)


def firm_reports(request):
    form = PartnerForm()
    title = 'Фирмен отчет'

    if request.method == 'POST':
        partner = request.POST.get('partner')
        print(request.POST)
        if int(partner) == 1:
            payload = {'records': '', 'total_sum': 'Няма такава фирма'}
            return render(request, template_name='show_reports.html', context=payload)

        if int(partner) == 2:
            result = Partner.objects.all().annotate(total = Sum('balance')).order_by('name')
            total = result[0].total
            payload = {'records': result, 'total': 'test'}
            return render(request, template_name='show_all_firms.html', context=payload)

        results = Record.objects.filter(partner_id=partner).order_by('id')
        total = results.reverse()[0].balance
        payload = {'records': results, 'total_sum': total}

        return render(request, template_name='show_reports.html', context=payload)

    context = {'title': title, 'form': form}
    return render(request, template_name='choice_reports.html', context=context)


@login_required(login_url='login')
def show_totals(request):
    total_sum = Record.objects.filter(order_type='C').aggregate(Sum('amount'))
    total = total_sum['amount__sum']
    payload = {'total_sum': total}
    return render(request, 'show_totals.html', context=payload)


def get_order(order_type):
    orders = Order.objects.first()

    date = datetime.now().month
    month_dict = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
                  7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}
    current_month = month_dict[date]
    db_month = orders.month

    counter = 0
    if order_type == 'A':
        counter = orders.al_counter + 1
        orders.al_counter = counter
    elif order_type == 'G':
        order_type = 'C'
        counter = orders.glass_counter + 1
        orders.glass_counter = counter
    elif order_type == 'P':
        counter = orders.pvc_counter + 1
        orders.pvc_counter = counter
    else:
        return ''

    orders.save()

    if current_month != db_month:
        orders.month = current_month
        orders.al_counter, orders.glass_counter, orders.pvc_counter = 1, 1, 1
        orders.save()
        counter = 1

    return f"{order_type}-{current_month}-{counter}"


def get_close_balance(partner_id, order_type, open_balance, amount):
    if partner_id == 1 or partner_id == 2:
        return 0

    if order_type in ['C', 'B']:
        return int(open_balance) + int(amount)
    else:
        return int(open_balance) - int(amount)

