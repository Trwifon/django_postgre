from django.db import models

# Create your models here.
from nadejda_94.records.choices import WarehouseChoices, OrderTypeChoices, PartnerTypeChoices



class Partner(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=PartnerTypeChoices.choices)
    balance = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    month = models.CharField(max_length=4)
    al_counter = models.PositiveSmallIntegerField(default=0)
    glass_counter = models.PositiveSmallIntegerField(default=0)
    pvc_counter = models.PositiveSmallIntegerField(default=0)


class Record(models.Model):
    warehouse = models.CharField(max_length=1, choices=WarehouseChoices)
    order_type = models.CharField(max_length=2, choices=OrderTypeChoices.choices)
    amount = models.IntegerField()
    balance = models.IntegerField()
    order = models.CharField(max_length=11, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    partner = models.ForeignKey(
        to=Partner,
        default=1000,
        on_delete=models.SET(1000),
        related_name='records'
    )

