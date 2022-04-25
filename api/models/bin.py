from django.db import models

class Bin(models.Model):
    barcode = models.IntegerField()
    active = models.BooleanField()
    bin_model_id = models.ForeignKey(
        'bin_model',
        on_delete=models.CASCADE
    )
    location_id = models.ForeignKey(
        'location',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"bin: {self.barcode} is located at {self.location_id} and Active Status = {self.active}"
    
    def as_dict(self):
        return {
            'id': self.id,
            'active': self.active,
            'bin_model_id': self.bin_model_id,
            'location_id': self.location_id
        }