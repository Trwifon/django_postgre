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

users_dict = {'Trifon': 'M', 'Tsonka': 'O', 'Elena': 'A', 'Diana': 'P', 'Nadya': 'G'}


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


def create_record(request, pk):
    form = RecordForm()
    partner = Partner.objects.get(id=pk)
    partner_name = partner.name
    open_balance = partner.balance
    title = f"Нов запис - фирма: {partner_name}, " \
            f"начално салдо: {open_balance} лв"


    if request.method == 'POST':
        form = RecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.warehouse = users_dict[request.user.username]
            record.balance = get_close_balance(
                pk,
                record.order_type,
                open_balance,
                record.amount
                )
            record.order = get_order(record.order_type)
            record.partner_id = pk

            if record.partner_id == 1:
                record.amount = -abs(record.amount)

            if 'bal' in request.POST:
                title = f"{title}, " \
                        f"крайно салдо: {record.balance}, " \
                        f"поръчка: {record.order}"

                context = {'title': title, 'form': form}
                return render(request, 'create_record.html', context)

            elif 'save' in request.POST:
                update_order(record.order_type)

                partner.balance = record.balance
                partner.save()

                record.save()
                return redirect('home')

    context = {'title': title,
               'partner_name': partner_name,
               'open_balance': open_balance,
               'form': form}
    return render(request, 'create_record.html', context)


def home(request):

    if not request.user.username:
        return redirect(login_page)

    results = Record.objects \
        .filter(created_at=datetime.today(), warehouse=users_dict[request.user.username]) \
        .order_by('id')

    total_sum = results.filter(order_type='C').aggregate(Sum('amount'))
    total = total_sum['amount__sum']

    partners = Partner.objects.all().order_by('name')

    form = PartnerForm()

    payload = {'records': results, 'total_sum': total, 'form': form}

    return render(request, template_name='home.html', context=payload)


def day_reports(request):
    form = WarehouseForm()
    title = 'Дневен отчет'

    if request.method == 'POST':
        current_warehouse = request.POST.get('warehouse')

        if request.user.username == 'Trifon' and current_warehouse == 'M':
            results = Record.objects \
                .filter(created_at=datetime.today()).order_by('id')
        elif request.user.username != 'Trifon' and current_warehouse == 'M':
            results = Record.objects\
                .filter(created_at=datetime.today(), warehouse=users_dict[request.user.username])\
                .order_by('id')
        else:
            results = Record.objects\
                .filter(created_at=datetime.today(), warehouse=current_warehouse)\
                .order_by('id')

        total_sum = results.filter(order_type='C').aggregate(Sum('amount'))
        total = total_sum['amount__sum']
        payload = {'records': results, 'total_sum': total, 'warehouse': current_warehouse}

        return render(request, template_name='show_reports.html', context=payload)

    context = {'title': title, 'form': form}
    return render(request, 'choices.html', context=context)


def firm_reports(request, pk: int):

    if pk == 1:
        payload = {'records': '', 'total_sum': 'Няма такава фирма'}
        return render(request, template_name='show_reports.html', context=payload)

    if pk == 2:
        result = Partner.objects.all().values('name', 'balance').order_by('name')
        df = pd.DataFrame(list(result))

        name = f"Firmi - {datetime.today().date()}"

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={name}.xlsx'

        df.to_excel(response, index=False, engine='openpyxl')

        return response

    results = Record.objects.filter(partner_id=pk).order_by('id')

    if results:
        total = results.reverse()[0].balance
    else:
        total = 0

    payload = {'records': results, 'total_sum': total}
    return render(request, template_name='show_reports.html', context=payload)


def month_reports(request):
    form = MonthWarehouseForm()
    title = "Месечен отчет"

    if request.method == 'POST':
        form = MonthWarehouseForm()
        warehouse = request.POST.get('warehouse')
        current_warehouse = warehouse if warehouse != 'M' else users_dict[request.user.username]
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


def partner_choice(request):
    form = PartnerForm()

    if request.method == 'POST':
        pk = request.POST.get('partner')

        if 'record' in request.POST:
            return redirect('create_record', pk)

        elif 'report' in request.POST:
            return redirect('firm_reports', pk)

    title = 'Избери фирма'
    context = {'title': title, 'form': form}
    return render(request, 'partner_choice.html', context)


def show_totals(request):
    total_sum = Record.objects.filter(order_type='C').aggregate(Sum('amount'))

    total = total_sum['amount__sum'] if request.user.username in ('Trifon', 'Anton') else 0

    payload = {'total_sum': total}
    return render(request, 'show_totals.html', context=payload)




