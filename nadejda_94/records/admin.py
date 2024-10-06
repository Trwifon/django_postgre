from django.contrib import admin

# Register your models here.
from nadejda_94.records.models import Partner, Order, Record


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'balance']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['month', 'al_counter', 'glass_counter', 'pvc_counter']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'warehouse', 'order_type', 'partner', 'amount', 'order', 'note']
    list_filter = ['id']