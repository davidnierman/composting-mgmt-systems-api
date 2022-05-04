from django.db import models

class Bin(models.Model):
    barcode = models.IntegerField()
    active = models.BooleanField()
    bin_model_foreign_key = models.ForeignKey(
        'bin_model',
        on_delete=models.CASCADE
    )
    location_id = models.ForeignKey(
        'location',
        on_delete=models.CASCADE
    )

    def model(self):
        return self.bin_model_foreign_key.name

    def __str__(self):
        return f"Barcode: {self.barcode} | model: {self.bin_model_id} | Location: {self.location_id} | Active = {self.active}"
    
    def as_dict(self):
        return {
            'id': self.id,
            'active': self.active,
            'bin_model_id': self.bin_model_id,
            'location_id': self.location_id
        }