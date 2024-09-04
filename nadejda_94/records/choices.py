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


class YearChoices(models.IntegerChoices):
    YEAR_FOUR = 2024, '2024'
    YEAR_FIVE = 2025, '2025'
    YEAR_SIX = 2026, '2026'
    YEAR_SEVEN = 2027, '2027'
    YEAR_EIGHT = 2028, '2028'
    YEAR_NINE = 2029, '2029'
    YEAR_TEN = 2030, '2030'


class MonthChoices(models.IntegerChoices):
    JANUARY = 1, '1'
    FEBRUARY = 2, '2'
    MARCH = 3, '3'
    APRIL = 4, '4'
    MAY = 5, '5'
    JUNE = 6, '6'
    JULY = 7, '7'
    AUGUST = 8, '8'
    SEPTEMBER = 9, '9'
    OCTOBER = 10, '10'
    NOVEMBER = 11, '11'
    DECEMBER = 12, '12'
