from django.db import models
from django.contrib.auth import get_user_model

class Route(models.Model):
    DAYS_CHOICES = [
        ('MONDAY', 'monday'),
        ('TUESDAY', 'tuesday'),
        ('WEDNESDAY', 'wednesday'),
        ('THURSDAY', 'thursday'),
        ('FRIDAY', 'friday')
    ]

    day_of_week = models.CharField(choices = DAYS_CHOICES, max_length=9)
    user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"this is {self.user_id} route that runs on {self.day_of_week}"

    def as_dict(self):
        return{
            'id': self.id,
            'day_of_week': self.day_of_week,
            'user_id': self.user_id
        }