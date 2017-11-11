import datetime
from django.db import models
from rentcar.validators import convert_date

CAR_GROUPS_CHOICES = (('Group A', 'Group A'), ('Group B', 'Group B'))
CAR_BRANDS_CHOICES = (('Renault', 'Renault'), ('Volkswagen', 'Volkswagen'))
CAR_ENERGY_CHOICES = (('Diesel', 'Diesel'), ('Petrol', 'Petrol'))
CAR_MECHANIC_CHOICES = (('Automatic', 'Automatic'), ('Manual', 'Manual'))


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
    mechanic = models.CharField(choices=CAR_MECHANIC_CHOICES, max_length=16)
    fuel = models.CharField(choices=CAR_ENERGY_CHOICES, max_length=16)
    available = models.BooleanField(default=True)

    @property
    def name(self):
        return str(self.brand) + ' ' + str(self.model)

    def __str__(self):
        return self.name


class Booking(models.Model):
    car = models.ForeignKey(Car)
    session = models.ForeignKey('sessions.Session')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    date_from = models.DateTimeField()
    date_until = models.DateTimeField()
    time_period = models.PositiveSmallIntegerField()
    total = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['-creation_date']


def search_available_cars(arrival_date, arrival_hours, arrival_minutes,
                          departure_date, departure_hours, departure_minutes):

    date_from = convert_date(arrival_date).replace(hour=int(arrival_hours), minute=int(arrival_minutes))
    date_until = convert_date(departure_date).replace(hour=int(departure_hours), minute=int(departure_minutes))
    cars = Car.objects.filter(available=True)
    available_cars = list()

    for car in cars:
        # only cars available must be appear in the search
        # only cars without a date_from in the desired period must appear in the search
        # only cars without a date_until in the desired period must appear in the search
        bookings = Booking.objects.filter(car=car)\
            .filter(date_from__gte=date_from).filter(date_from__lte=date_until)\
            .filter(date_until__gte=date_from).filter(date_until__lte=date_until)
        if not bookings:
            available_cars.append(car)

    print(date_from, date_until)
    print(cars, available_cars)
    print(bookings)
    return available_cars

