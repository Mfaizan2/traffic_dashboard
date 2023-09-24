from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Vehicle model to save vehicles data
class Vehicle(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]


# Sensor model to save sensors data
class SensorData(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="sensors",
    )
    latitude = models.FloatField(
        validators=[
            MinValueValidator(limit_value=-90.0),
            MaxValueValidator(limit_value=90.0),
        ]
    )
    longitude = models.FloatField(
        validators=[
            MinValueValidator(limit_value=-180.0),
            MaxValueValidator(limit_value=180.0),
        ]
    )
    timestamp = models.DateTimeField()
    vehicle_speed = models.FloatField()
    speed_limit = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["latitude"]),
            models.Index(fields=["longitude"]),
            models.Index(fields=["timestamp"]),
        ]
