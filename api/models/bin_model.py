from django.db import models

class Bin_Model(models.Model):
    MATERIAL_CHOICES = [
        ('PLASTIC', 'plastic'),
        ('METAL', 'metal')
    ]

    COLOR_CHOICES = [
        ('FORREST-GREEN', 'forrest-green'),
        ('OLIVE-GREEN', 'olive-green'),
        ('SPRING-GREEN',  'spring-green')
    ]

    name = models.CharField(max_length=50)
    material  = models.CharField(choices = MATERIAL_CHOICES, max_length=7)
    color = models.CharField(choices = COLOR_CHOICES, max_length=14 )
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    volume_gallons = models.IntegerField()
    weight_lbs = models.IntegerField()

    def __str__(self):
        return self.name

    def as_dict(self):
        return{
            'name' :self.name,
            'material' : self.material,
            'color' : self.color,
            'length' : self.length,
            'width' : self.width,
            'height' : self.height,
            'volume_gallons' : self.volume_gallons,
            'weight_lbs' : self.weight_lbs
        }


