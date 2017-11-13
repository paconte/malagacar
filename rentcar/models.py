from django.db import models

CAR_GROUPS_CHOICES = (('Group A', 'Group A'), ('Group B', 'Group B'))
CAR_BRANDS_CHOICES = (('Renault', 'Renault'), ('Volkswagen', 'Volkswagen'))
CAR_ENERGY_CHOICES = (('Diesel', 'Diesel'), ('Petrol', 'Petrol'))
# CAR_MECHANIC_CHOICES = (('Automatic', 'Automatic'), ('Manual', 'Manual'))


class CarGroup(models.Model):
    """
    Model to categorized cars and it price.

    :name: Name of the group e.g Group A.
    :day_price: Price per day when booking a car belonging to this Group.
    """
    name = models.CharField(choices=CAR_GROUPS_CHOICES, max_length=16)
    day_price = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.name)


class Car(models.Model):
    """
    Model for representing available cars.

    properties:
    :name: Returns the representing name of the car combining the brand and model.
    """
    group = models.ForeignKey(CarGroup)
    brand = models.CharField(choices=CAR_BRANDS_CHOICES, max_length=32)
    model = models.CharField(max_length=32)
    places = models.PositiveSmallIntegerField()
    air_conditioning = models.BooleanField(default=True)
    automatic = models.BooleanField(default=False)
    fuel = models.CharField(choices=CAR_ENERGY_CHOICES, max_length=16)

    @property
    def name(self):
        return str(self.brand) + ' ' + str(self.model)

    def __str__(self):
        return self.name


class CarInventory(models.Model):
    car = models.ForeignKey(Car)
    quantity = models.PositiveSmallIntegerField(default=0)
    available = models.PositiveSmallIntegerField(default=0)


class Booking(models.Model):
    car = models.ForeignKey(Car)
