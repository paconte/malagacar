from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from rentcar.forms import SearchForm, BookingForm
from rentcar.models import search_available_cars, get_car, Booking
from rentcar.validators import calculate_total_rent_days, convert_dates, date_to_string, extract_time_from_date


def index(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            a, b, c, d, e, f = _get_dates_arguments(request)
            # get available cars for given dates
            available_cars = search_available_cars(a, b, c, d, e, f)
            # calculate the total numbers of days the car is hired
            rent_days = calculate_total_rent_days(a, b, c, d, e, f)
            # calculate the cost of hiring the cars for the total numbers of days
            prices = list()
            for car in available_cars:
                prices.append(car.calculate_price(rent_days))
            # create booking form
            booking_forms = list()
            for car in available_cars:
                date_from, date_until = convert_dates(a, b, c, d, e, f)
                price = car.calculate_price(rent_days)
                reservation = Booking(date_from=date_from, date_until=date_until, time_period=rent_days,
                                      car=car, total=price)
                booking_form = BookingForm(instance=reservation)
                booking_forms.append(booking_form)

            # add prices to the available cars
            cars_with_prices = zip(available_cars, prices)
            # render
            return render(request, 'landing.html', {'form': search_form, 'available_cars': cars_with_prices})
        else:
            return render(request, 'landing.html', {'form': search_form})
    else:
        return render(request, 'landing.html', {'form': SearchForm()})


def booking(request, car_id):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            # retrieve the car data from db
            car = _get_car(request, car_id, search_form)
            # calculate the dates
            a, b, c, d, e, f = _get_dates_arguments(request)
            date_from, date_until = convert_dates(a, b, c, d, e, f)
            str_date_from = date_to_string(date_from)
            str_date_until = date_to_string(date_until)
            str_time_from = extract_time_from_date(date_from)
            str_time_until = extract_time_from_date(date_until)
            # calculate price and total rented days
            rent_days = calculate_total_rent_days(a, b, c, d, e, f)
            price = car.calculate_price(rent_days)
            # pre fill out the reservation
            reservation = Booking(date_from=date_from, date_until=date_until, time_period=rent_days,
                                  car=car, total=price)
            booking_form = BookingForm(instance=reservation)

            return render(request, 'booking.html',
                          {'car': car, 'booking_form': booking_form,
                           'str_date_from': str_date_from, 'str_date_until': str_date_until,
                           'str_time_from': str_time_from, 'str_time_until': str_time_until})
        else:
            return render(request, 'landing.html', {'form': search_form})
    else:
        return render(request, 'landing.html', {'form': SearchForm()})


def booking_confirmation(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            return render(request, 'confirmation.html')
        else:
            return render(request, 'booking.html', {'booking_form': booking_form})


def _get_dates_arguments(request):
    return (request.POST['arrival_date'], request.POST['arrival_hours'], request.POST['arrival_minutes'],
            request.POST['departure_date'], request.POST['departure_hours'], request.POST['departure_minutes'])


def _get_car(request, car_id, search_form):
    try:
        car = get_car(car_id)
    except ObjectDoesNotExist:
        return render(request, 'landing.html', {'form': search_form})
    except MultipleObjectsReturned:
        return render(request, 'landing.html', {'form': search_form})
    return car

