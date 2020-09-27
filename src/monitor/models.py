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
    date_added = models.DateTimeField(default=timezone.now())

    xi = models.FloatField(null=True)
    xa = models.FloatField(null=True)
    yi = models.FloatField(null=True)
    ya = models.FloatField(null=True)

    land_category = models.CharField(max_length=100, null=True)
    fire_status = models.CharField(max_length=3, default='BRN', choices=POINT_STATUS)

    nearest_city_distance = models.FloatField(null=True)
    city = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)

    satelite_image = models.ImageField(default='default.jpg', upload_to='satelites')
    # fyre_type_prediction_result
    # Smoke and fire mask
    # Earth category by API or MODEL
    def __str__(self):
        return f"{self.xi} - {self.xa} - {self.yi} - {self.ya}"


class FireObject(models.Model):
    date_added = models.DateTimeField(default=timezone.now())
    image = models.ImageField(default='default.jpg', upload_to='fires')
    x_min = models.FloatField(null=True)
    x_max = models.FloatField(null=True)
    y_min = models.FloatField(null=True)
    y_max = models.FloatField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['x_min', 'x_max', 'y_min', 'y_max'], name='unique fire')
        ]


class FireInfo(models.Model):
    thermal_point = models.ForeignKey(ThermalPoint, on_delete=models.CASCADE)
    fire_object = models.ForeignKey(FireObject, on_delete=models.CASCADE)
    fire_type = models.ForeignKey(FireType, on_delete=models.CASCADE, null=True)

# TODO model region -> city with same shit from osm nominative

# TODO model result should be here
# class FireModelsResult(models.Model):
#