from django.db import models


class WarehouseChoices(models.TextChoices):
    ALUMINUM = 'A', 'Алуминий'
    GLASS = 'G', 'Стъклопакети'
    PVC = 'P', 'PVC'
    ORDERS = 'O', 'Поръчки'
    MANAGER = 'M', 'Управител'


class OrderTypeChoices(models.TextChoices):
    CASH = 'C', 'Каса'
    BANK = 'B', 'Банка'
    SELL = 'S', 'Продажба'
    ORDER_ALUMINUM = 'A', 'Поръчка Алуминий'
    ORDER_GLASS = 'G', 'Поръчка Стъклопакети'
    ORDER_PVC = 'P', 'Поръчка PVC'


class PartnerTypeChoices(models.TextChoices):
    SUPPLIER = 'S', 'Доставчик'
    FIRM = 'F', 'Фирма'
    RETAIL_CUSTOMER = 'RC', 'Клиент на дребно'
