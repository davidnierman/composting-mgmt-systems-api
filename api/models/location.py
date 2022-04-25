from django.db import models
from django.contrib.auth import get_user_model

class Location(models.Model):
    LOCATION_TYPE_CHOICES  = ['warehouse', 'residential', 'commercial' ]

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField
    type = models.CharField(choices=LOCATION_TYPE_CHOICES)
    user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    route_id = models.ForeignKey(
        'route', # might have to change this later to reference the app it is in https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"The Locations is a {self.type} location and can be found at: \n {self.street} \n {self.city} {self.state} {self.zip_code}"

    def as_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'state': self.state,
            'zip_code': self.zip_code,
            'type': self.type,
            'user_id': self.user_id,
            'route_id': self.route_id
            }