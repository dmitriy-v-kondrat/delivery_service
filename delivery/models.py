
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Location(models.Model):
    """
    A model to represent a geographic location.

    Attributes:
        zip_code (str): The ZIP code of the location (unique).
        city (str): The city name.
        state (str): The state name.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.

    Methods:
        __str__(): Returns the ZIP code as the string representation of the location.

    """
    zip_code = models.CharField(max_length=5, unique=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.zip_code


class Cargo(models.Model):
    """
    A model to represent cargo information.

    Attributes:
        pick_up (ForeignKey): The location where the cargo will be picked up.
        delivery (ForeignKey): The location where the cargo will be delivered.
        weight (int): The weight of the cargo (1 to 1000 pounds).
        description (str): A description of the cargo.

    Methods:
        __str__(): Returns the ZIP code of the pick-up location as the string representation of the cargo.

    """
    pick_up = models.ForeignKey(Location, on_delete=models.CASCADE,
                                to_field='zip_code', related_name='pick_up'
                                )
    delivery = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 to_field='zip_code', related_name='delivery'
                                 )
    weight = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1),
                                                                     MaxValueValidator(1000)]
                                              )
    description = models.TextField()

    def __str__(self):
        return str(self.pick_up)


class Truck(models.Model):
    """
    A model to represent a truck.

    Attributes:
        number (str): The truck's unique identifier (5 characters).
        location (ForeignKey): The location where the truck is currently located.
        carrying_capacity (int): The maximum carrying capacity of the truck (1 to 1000 pounds).

    Methods:
        __str__(): Returns the truck's number as the string representation of the truck.

    """
    number = models.CharField(max_length=5, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 to_field='zip_code', related_name='locations'
                                 )
    carrying_capacity = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1),
                                                                                MaxValueValidator(1000)]
                                                         )

    def __str__(self):
        return str(self.number)
