from django.db import models
from django.contrib.auth import get_user_model

class Order_Bin(models.Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'processing'),
        ('DELIVERED', 'delivered'),
    ]

    order_date = models.DateField()
    fulfilled_date = models.DateField()
    status = models.CharField(choices = STATUS_CHOICES, max_length=10)
    location_id = models.ForeignKey(
        'location',
        on_delete=models.CASCADE
    )
    bin_model_id = models.ForeignKey(
        'bin_model',
        on_delete=models.CASCADE
    )

