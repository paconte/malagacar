from django.db import models
from rentcar.validators import convert_dates, policy_read_validator
from django_countries.fields import CountryField


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

    def calculate_price(self, days):
        return days * self.group.day_price


class Booking(models.Model):
    car = models.ForeignKey(Car)
    # session = models.ForeignKey('sessions.Session')
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    date_from = models.DateTimeField()
    date_until = models.DateTimeField()
    time_period = models.PositiveSmallIntegerField()
    total = models.DecimalField(max_digits=8, decimal_places=2)

    forename = models.CharField(max_length=24, verbose_name='First name')
    surname = models.CharField(max_length=24, verbose_name='Last name')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=64, verbose_name='Phone')
    address = models.CharField(max_length=256, verbose_name='Address')
    city = models.CharField(max_length=128, verbose_name='City')
    zip_code = models.CharField(max_length=256, verbose_name='ZIP/Postal code')
    country = CountryField(max_length=2, verbose_name='Country')
    comments = models.TextField(max_length=1024, verbose_name='Comments', blank=True)
    policy_read = models.BooleanField(default=False, validators=[policy_read_validator])

    class Meta:
        ordering = ['-creation_date']


def search_available_cars(arrival_date, arrival_hours, arrival_minutes,
                          departure_date, departure_hours, departure_minutes):

    date_from, date_until = convert_dates(
        arrival_date, arrival_hours, arrival_minutes, departure_date, departure_hours, departure_minutes)
    cars = Car.objects.filter(available=True)
    available_cars = list()

    for car in cars:
        if check_car_is_available(car, date_from, date_until):
            available_cars.append(car)

    return available_cars


def check_car_is_available(car_id,
                           arrival_date, arrival_hours, arrival_minutes,
                           departure_date, departure_hours, departure_minutes):
    result = False
    date_from, date_until = convert_dates(
        arrival_date, arrival_hours, arrival_minutes, departure_date, departure_hours, departure_minutes)
    car = Car.objects.get(pk=car_id)

    if car.available and check_car_is_available(car, date_from, date_until):
        result = True

    return result


def check_car_is_available(car, date_from, date_until):
    # only cars available must be appear in the search
    # only cars without a date_from in the desired period must appear in the search
    # only cars without a date_until in the desired period must appear in the search
    result = False
    bookings = Booking.objects.filter(car=car) \
        .filter(date_from__gte=date_from).filter(date_from__lte=date_until) \
        .filter(date_until__gte=date_from).filter(date_until__lte=date_until)
    if not bookings:
        result = True
    return result


def get_car(car_id):
    return Car.objects.get(pk=car_id)


