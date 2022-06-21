from django.db import models
from django.contrib.auth import get_user_model

class Location(models.Model):
    LOCATION_TYPE_CHOICES  = [
    ('WAREHOUSE', 'warehouse'),
    ('RESIDENTIAL', 'residential'),
    ('COMMERICAL', 'commercial'),
]

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    property_type = models.CharField(choices=LOCATION_TYPE_CHOICES, max_length=11)
    user_foreign_key = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    route = models.ForeignKey(
        'Route', # might have to change this later to reference the app it is in https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey
        on_delete=models.CASCADE,
        blank=True,
        default='',
        null=True
    )


    def email(self):
        return self.user_foreign_key.email

    def __str__(self):
        return f"The Locations is a {self.property_type} location and can be found at: \n {self.street}"

    def as_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'property_type': self.property_type,
            'user_foreign_key': self.email(), 
            'route': self.route
            }