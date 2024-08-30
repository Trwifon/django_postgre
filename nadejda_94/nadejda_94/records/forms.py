from django.forms import ModelForm
from django import forms
from .choices import WarehouseChoices
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


class PartnerForm(forms.ModelForm):
    partner = forms.ModelChoiceField(
        queryset=Partner.objects.all().order_by('name'),
        label='Фирма',
    )
    class Meta:
        model = Partner
        fields = ['partner']


class WarehouseForm(forms.Form):
    warehouse = forms.ChoiceField(
        choices=WarehouseChoices.choices,
        label='Склад'
    )


