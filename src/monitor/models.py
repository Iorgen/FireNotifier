from django.db import models
from django.utils import timezone


# TODO fill static table
class FireType(models.Model):
    name = models.CharField(max_length=100)


# TODO fill static table
class LandCategory(models.Model):
    name = models.CharField(max_length=100)


# Create your models here.
class ThermalPoint(models.Model):

    POINT_STATUS = [
        ('EXT', 'extinguished'),
        ('BRN', 'burning')
    ]
    xi = models.FloatField()
    xa = models.FloatField()
    yi = models.FloatField()
    ya = models.FloatField()

    land_category = models.ForeignKey(LandCategory, on_delete=models.CASCADE)
    fire_status = models.CharField(max_length=3, default='BRN', choices=POINT_STATUS)

    def __str__(self):
        return f"{self.xi} - {self.xa} - {self.yi} - {self.ya}"


class FireObject(models.Model):
    date_added = models.DateTimeField(default=timezone.now())
    image = models.ImageField(default='default.jpg', upload_to='fires')


class FireInfo(models.Model):
    thermal_point = models.ForeignKey(ThermalPoint, on_delete=models.CASCADE)
    fire_object = models.ForeignKey(FireObject, on_delete=models.CASCADE)
    fire_type = models.ForeignKey(FireType, on_delete=models.CASCADE)


# TODO model result should be here
# class FireSpreadResult(models.Model):
#