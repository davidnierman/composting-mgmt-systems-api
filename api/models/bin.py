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

    def location(self):
        return self.location_id.street +" "+ self.location_id.city +" "+ self.location_id.state +", "+ self.location_id.zip_code

    def __str__(self):
        return f"Barcode: {self.barcode} | model: {self.bin_model_id} | Location: {self.location_id} | Active = {self.active}"
    
    def as_dict(self):
        return {
            'id': self.id,
            'active': self.active,
            'model': Bin.objects.select_related('bin_model_foreign_key').get(id=self.id).bin_model_foreign_key.as_dict(),
            'location': Bin.objects.select_related('location_id').get(id=self.id).location_id.as_dict()
        }