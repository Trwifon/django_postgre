from django.forms import ModelForm
from django import forms
from .choices import WarehouseChoices, OrderTypeChoices, YearChoices, MonthChoices
from .models import Record, Partner


class RecordForm(ModelForm):
    partner = forms.ModelChoiceField(
        queryset=Partner.objects.all().order_by('name'),
        label='Фирма',
    )

    class Meta:
        model = Record
        fields = [
            'partner',
            'order_type',
            'amount',
            'note',
        ]

        labels = {
            'order_type': 'Вид',
            'amount': 'Сума',
            'note': 'Забележка'
        }


class PartnerForm(ModelForm):
    partner = forms.ModelChoiceField(
        queryset=Partner.objects.all().order_by('name'),
        label='Фирма',
    )
    class Meta:
        model = Partner
        fields = ['partner']


class NewPartnerForm(ModelForm):
    class Meta:
        model = Partner
        exclude = ['type']
        labels = {
            'name': 'Име',
            'balance': 'Салдо',
        }


class WarehouseForm(forms.Form):
    warehouse = forms.ChoiceField(
        choices=WarehouseChoices.choices,
        label='Склад'
    )


class MonthWarehouseForm(WarehouseForm):
    year = forms.ChoiceField(
        choices=YearChoices.choices,
        label='Година'
    )

    month = forms.ChoiceField(
        choices=MonthChoices.choices,
        label='Месец'
    )




