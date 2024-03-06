from django.db import models

class ConditionChoices(models.TextChoices):
    NEW = 'New'
    USED_EXCELLENT = 'Used - Excellent'
    USED_GOOD = 'Used - Good'
    USED_FAIR = 'Used - Fair'
    USED_POOR = 'Used - Poor'

class DurationChoices(models.IntegerChoices):
    TWO_DAYS = 2
    THREE_DAYS = 3
    FIVE_DAYS = 5
    SEVEN_DAYS = 7
    TEN_DAYS = 10

class PackageTypeChoices(models.TextChoices):
    BOX = 'Box'
    ENVELOPE = 'Envelope'

class WeightRangeChoices(models.TextChoices):
    UPTO_2_KG = '0-2'
    UPTO_5_KG = '2-5'
    UPTO_10_KG = '5-10'
    UPTO_20_KG = '10-20'

class CarrierTypeChoices(models.TextChoices):
    COURIER = 'Courier'
    AIR_FREIGHT = 'Air Freight'
    TRUCKING = 'Trucking'



SHIPPING_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )