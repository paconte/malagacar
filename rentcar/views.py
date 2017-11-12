from django.shortcuts import render

from rentcar.forms import SearchForm
from rentcar.models import search_available_cars, get_car
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
            a, b, c, d, e, f = _get_dates_arguments(request)

            car = get_car(car_id)

            date_from, date_until = convert_dates(a, b, c, d, e, f)
            str_date_from = date_to_string(date_from)
            str_date_until = date_to_string(date_until)
            str_time_from = extract_time_from_date(date_from)
            str_time_until = extract_time_from_date(date_until)

            rent_days = calculate_total_rent_days(a, b, c, d, e, f)
            price = car.calculate_price(rent_days)

            return render(request, 'booking.html',
                          {'car': car, 'date_from': date_from, 'date_until': date_until,
                           'str_date_from': str_date_from, 'str_date_until': str_date_until,
                           'str_time_from': str_time_from, 'str_time_until': str_time_until,
                           'rent_days': rent_days, 'price': price})
        else:
            return render(request, 'landing.html', {'form': SearchForm()})
    else:
        return render(request, 'landing.html', {'form': SearchForm()})


def _get_dates_arguments(request):
    return (request.POST['arrival_date'], request.POST['arrival_hours'], request.POST['arrival_minutes'],
            request.POST['departure_date'], request.POST['departure_hours'], request.POST['departure_minutes'])
