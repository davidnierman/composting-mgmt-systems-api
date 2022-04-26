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
    zip_code = models.IntegerField
    property_type = models.CharField(choices=LOCATION_TYPE_CHOICES, max_length=11)
    user = models.ForeignKey(
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

    def __str__(self):
        return f"The Locations is a {self.property_type} location and can be found at: \n {self.street} \n {self.city} {self.state} {self.zip_code}"

    def as_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'state': self.state,
            'zip_code': self.zip_code,
            'property_type': self.property_type,
            'user_id': self.user,
            'route_id': self.route
            }