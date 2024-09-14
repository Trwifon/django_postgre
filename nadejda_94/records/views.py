from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
from .forms import RecordForm, PartnerForm, WarehouseForm, MonthWarehouseForm, NewPartnerForm
from .helpers import get_order, get_close_balance, update_order
from .models import Record, Partner, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd

CURRENT_WAREHOUSE = 'M'

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
            order_type = form.instance.order_type
            amount = form.cleaned_data['amount']
            open_balance = partner.balance

            current_order = get_order(order_type)
            amount = -abs(int(amount)) if partner_id == 1 else amount
            close_balance = get_close_balance(partner_id, order_type, open_balance, amount)

            if 'bal' in request.POST:
                title = f"Начално салдо: {open_balance}, Крайно салдо: {close_balance}, Поръчка: {current_order}"

                context = {'title': title, 'form': form}
                return render(request, 'create_record.html', context)

            else:
                title = 'Save'

                form.instance.partner = partner
                form.instance.amount = amount
                form.instance.balance = close_balance
                form.instance.order = current_order
                form.save()

                partner.balance = close_balance
                partner.save()

                update_order(order_type)

                return redirect('home')

    context = {'title': title, 'form': form}
    return render(request, 'create_record.html', context)


def home(request):
    results = Record.objects \
        .filter(created_at=datetime.today(), warehouse=CURRENT_WAREHOUSE) \
        .order_by('id')

    # results = Record.objects \
    #     .filter(created_at="2024-08-30", warehouse=CURRENT_WAREHOUSE) \
    #     .order_by('id')

    total_sum = results.filter(order_type='C').aggregate(Sum('amount'))
    total = total_sum['amount__sum']

    partners = Partner.objects.all().order_by('name')

    payload = {'records': results, 'total_sum': total}

    return render(request, template_name='home.html', context=payload)


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
    return render(request, 'choices.html', context=context)


def firm_reports(request):
    form = PartnerForm()
    title = 'Фирмен отчет'

    if request.method == 'POST':
        partner = request.POST.get('partner')
        if int(partner) == 1:
            payload = {'records': '', 'total_sum': 'Няма такава фирма'}
            return render(request, template_name='show_reports.html', context=payload)

        if int(partner) == 2:
            result = Partner.objects.all().values('name', 'balance').order_by('name')
            df = pd.DataFrame(list(result))

            name = f"Firmi - {datetime.today().date()}"

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={name}.xlsx'

            df.to_excel(response, index=False, engine='openpyxl')

            return response

            # payload = {'records': result}
            # return render(request, template_name='show_all_firms.html', context=payload)

        results = Record.objects.filter(partner_id=partner).order_by('id')

        if results:
            total = results.reverse()[0].balance
        else:
            total = 0

        payload = {'records': results, 'total_sum': total}
        return render(request, template_name='show_reports.html', context=payload)

    context = {'title': title, 'form': form}
    return render(request, template_name='choices.html', context=context)


def month_reports(request):
    form = MonthWarehouseForm()
    title = "Месечен отчет"

    if request.method == 'POST':
        form = MonthWarehouseForm()
        current_warehouse = request.POST.get('warehouse')
        current_warehouse = current_warehouse if current_warehouse != 'M' else CURRENT_WAREHOUSE
        current_year = request.POST.get('year')
        current_month = request.POST.get('month')

        results = Record.objects.\
            filter(warehouse=current_warehouse,
                   created_at__year=current_year,
                   created_at__month=current_month).\
            order_by('id')

        payload = {'records': results}
        return render(request, template_name='show_reports.html', context=payload)

    context = {'title': title, 'form': form}
    return render(request, template_name='choices.html', context=context)


def new_partner(request):
    form = NewPartnerForm()
    title = 'Нова фирма'

    if request.method == 'POST':
        form = NewPartnerForm(request.POST)

        if not form.is_valid():
            return HttpResponse('В базата вече има фирма с това име')

        form.save()

        return HttpResponse('Нов потребител')

    context = {'title': title, 'form': form}
    return render(request, template_name='choices.html', context=context)


@login_required(login_url='login')
def show_totals(request):
    total_sum = Record.objects.filter(order_type='C').aggregate(Sum('amount'))
    total = total_sum['amount__sum']
    payload = {'total_sum': total}
    return render(request, 'show_totals.html', context=payload)



